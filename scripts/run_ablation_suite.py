#!/usr/bin/env python
"""Ablation suite runner for query-phase experiments.

Runs multiple ablation variants by calling run_ab00.py as isolated subprocesses
with different environment variable overrides. Requires an existing Neo4j graph
(run with --no-builder).

Usage:
    python scripts/run_ablation_suite.py               # Run all variants
    python scripts/run_ablation_suite.py --studies AB-01 AB-02   # Specific studies
    python scripts/run_ablation_suite.py --max-samples 5 --no-ragas  # Quick test
    python scripts/run_ablation_suite.py --dry-run    # Print plan, do not run
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ── Ablation suite definition ─────────────────────────────────────────────────
# Format: (study_id, env_overrides, description)
# AB-00 is the baseline (already run separately).
QUERY_ABLATION_SUITE: list[dict] = [
    {
        "study_id": "AB-01",
        "description": "Vector-only retrieval — no BM25, no graph traversal",
        "env_overrides": {"RETRIEVAL_MODE": "vector"},
    },
    {
        "study_id": "AB-02",
        "description": "BM25-only retrieval — no vector, no graph traversal",
        "env_overrides": {"RETRIEVAL_MODE": "bm25"},
    },
    {
        "study_id": "AB-03",
        "description": "Reranker ON — bge-reranker-large (top_k=10)",
        "env_overrides": {"ENABLE_RERANKER": "true"},
    },
    {
        "study_id": "AB-04",
        "description": "Hallucination grader OFF — skip self-RAG check",
        "env_overrides": {"ENABLE_HALLUCINATION_GRADER": "false"},
    },
    {
        "study_id": "AB-05",
        "description": "Reranker ON + Vector-only — reranker over dense pool",
        "env_overrides": {"RETRIEVAL_MODE": "vector", "ENABLE_RERANKER": "true"},
    },
]


def _run_variant(
    study: dict,
    max_samples: int | None,
    ragas: bool,
    ragas_model: str,
    dataset: Path,
    dry_run: bool,
) -> dict | None:
    """Run a single ablation variant as a subprocess and return its result dict."""
    study_id = study["study_id"]
    env_overrides = study["env_overrides"]
    description = study["description"]

    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_tag = f"{study_id.lower()}-{timestamp_str}"

    cmd = [
        sys.executable,
        str(ROOT / "scripts" / "run_ab00.py"),
        "--no-builder",
        "--study-id", study_id,
        "--run-tag",
        run_tag,
        "--dataset",
        str(dataset),
    ]
    if max_samples is not None:
        cmd += ["--max-samples", str(max_samples)]
    if ragas:
        cmd += ["--ragas", "--ragas-model", ragas_model]

    env_display = "  ".join(f"{k}={v}" for k, v in env_overrides.items()) or "(none)"
    print()
    print("=" * 70)
    print(f"  {study_id}: {description}")
    print(f"  Env overrides: {env_display}")
    print(f"  Run tag: {run_tag}")
    print("=" * 70)

    if dry_run:
        print(f"  [DRY RUN] Would execute: {' '.join(cmd)}")
        return None

    import os

    env = {**os.environ, **env_overrides}

    result = subprocess.run(cmd, env=env, cwd=str(ROOT))
    if result.returncode != 0:
        print(f"\n  !! {study_id} FAILED (exit code {result.returncode})")
        return {"study_id": study_id, "error": f"exit_code={result.returncode}"}

    # Find the most recent JSON result for this run_tag
    runs_dir = ROOT / "notebooks" / "ablation" / "ablation_results" / "runs"
    candidates = sorted(runs_dir.glob(f"{study_id}.{run_tag}.json"), reverse=True)
    if not candidates:
        print(f"  !! Could not find result JSON for run_tag={run_tag}")
        return {"study_id": study_id, "error": "result_file_not_found"}

    data = json.loads(candidates[0].read_text())
    data["study_id"] = study_id  # Override to use suite ID
    data["study_description"] = description
    return data


def _print_comparison(results: list[dict], baseline: dict | None) -> None:
    """Print a formatted comparison table of all runs."""
    all_results = []
    if baseline:
        b = dict(baseline)
        b["study_id"] = "AB-00 (baseline)"
        all_results.append(b)
    all_results.extend(results)

    print()
    print("=" * 90)
    print("  ABLATION SUITE COMPARISON")
    print("=" * 90)

    header = f"{'Study':<20} {'Grounded':>8} {'GT_cov':>7} {'faith':>6} {'ans_rel':>8} {'ctx_prec':>9} {'ctx_rec':>8}"
    print(header)
    print("-" * 90)

    for r in all_results:
        sid = r.get("study_id", "?")
        if "error" in r:
            print(f"{sid:<20}  ERROR: {r['error']}")
            continue
        q = r.get("query", {})
        ragas = r.get("ragas", {})
        grounded = f"{q.get('grounded_count', 0)}/{q.get('total_questions', 0)}"
        gt_cov = f"{q.get('avg_gt_coverage', 0):.0%}"
        faith = f"{ragas.get('faithfulness', 0):.4f}" if ragas else "  - "
        ar = f"{ragas.get('answer_relevancy', 0):.4f}" if ragas else "  - "
        cp = f"{ragas.get('context_precision', 0):.4f}" if ragas else "  - "
        cr = f"{ragas.get('context_recall', 0):.4f}" if ragas else "  - "
        print(f"{sid:<20} {grounded:>8} {gt_cov:>7} {faith:>6} {ar:>8} {cp:>9} {cr:>8}")

    print()


def main() -> None:
    parser = argparse.ArgumentParser(description="Run ablation suite over query variants")
    parser.add_argument(
        "--studies",
        nargs="+",
        help="Study IDs to run (default: all). E.g. --studies AB-01 AB-02",
    )
    parser.add_argument(
        "--max-samples",
        type=int,
        default=15,
        help="Limit evaluation to N samples per variant (default: 15)",
    )
    parser.add_argument(
        "--no-ragas",
        action="store_true",
        help="Disable RAGAS evaluation (faster, no API cost)",
    )
    parser.add_argument(
        "--ragas-model",
        type=str,
        default="gpt-4.1-mini",
        help="Model for RAGAS evaluator",
    )
    parser.add_argument(
        "--dataset",
        type=Path,
        default=ROOT / "tests/fixtures/01_basics_ecommerce/gold_standard.json",
        help="Path to gold standard dataset",
    )
    parser.add_argument(
        "--baseline-json",
        type=Path,
        default=None,
        help="Path to AB-00 baseline JSON for comparison table",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print plan without executing",
    )
    args = parser.parse_args()

    # Filter suite if specific studies requested
    suite = QUERY_ABLATION_SUITE
    if args.studies:
        ids = set(args.studies)
        suite = [s for s in suite if s["study_id"] in ids]
        if not suite:
            print(f"No matching studies found. Available: {[s['study_id'] for s in QUERY_ABLATION_SUITE]}")
            sys.exit(1)

    ragas = not args.no_ragas

    print()
    print("=" * 70)
    print("  ABLATION SUITE RUNNER")
    print("=" * 70)
    print(f"  Studies:       {[s['study_id'] for s in suite]}")
    print(f"  Max samples:   {args.max_samples}")
    print(f"  RAGAS:         {'ENABLED' if ragas else 'DISABLED'}")
    print(f"  Dataset:       {args.dataset}")
    print(f"  Dry run:       {args.dry_run}")
    print()

    # Load baseline for comparison
    baseline = None
    if args.baseline_json and args.baseline_json.exists():
        baseline = json.loads(args.baseline_json.read_text())
    else:
        # Auto-find most recent AB-00 run
        runs_dir = ROOT / "notebooks" / "ablation" / "ablation_results" / "runs"
        candidates = sorted(runs_dir.glob("AB-00.run-*.json"), reverse=True)
        if candidates:
            baseline = json.loads(candidates[0].read_text())
            print(f"  Using baseline: {candidates[0].name}")

    results = []
    for study in suite:
        r = _run_variant(
            study,
            max_samples=args.max_samples,
            ragas=ragas,
            ragas_model=args.ragas_model,
            dataset=args.dataset,
            dry_run=args.dry_run,
        )
        if r and "error" not in r:
            results.append(r)
        elif r:
            results.append(r)

    if not args.dry_run:
        _print_comparison(results, baseline)

        # Save suite summary
        summary_dir = ROOT / "notebooks" / "ablation" / "ablation_results" / "suite"
        summary_dir.mkdir(parents=True, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        summary_file = summary_dir / f"suite_{ts}.json"
        summary = {
            "timestamp": datetime.now().isoformat(),
            "max_samples": args.max_samples,
            "ragas_enabled": ragas,
            "baseline": baseline,
            "results": results,
        }
        summary_file.write_text(json.dumps(summary, indent=2, default=str))
        print(f"  Suite summary saved to: {summary_file}")


if __name__ == "__main__":
    main()
