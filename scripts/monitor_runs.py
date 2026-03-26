#!/usr/bin/env python
"""Quick monitor for tracking multiple runs."""

import json
from pathlib import Path
from datetime import datetime

RUNS_DIR = Path("notebooks/ablation/ablation_results/runs")
SUITE_DIR = Path("notebooks/ablation/ablation_results/suite")

def check_runs():
    """Report status of recent runs."""
    # Check for AB-01 through AB-05 runs
    studies = {}
    for study_id in ["AB-01", "AB-02", "AB-03", "AB-04", "AB-05"]:
        candidates = sorted(RUNS_DIR.glob(f"{study_id}.run-*.json"), reverse=True)
        if candidates:
            data = json.loads(candidates[0].read_text())
            q = data.get("query", {})
            ragas = data.get("ragas", {})
            studies[study_id] = {
                "file": candidates[0].name,
                "grounded": f"{q.get('grounded_count', 0)}/{q.get('total_questions', 0)}",
                "faith": f"{ragas.get('faithfulness', 0):.4f}" if ragas else "pending",
            }
    
    # Check for e2e run
    e2e = None
    all_runs = sorted(RUNS_DIR.glob("AB-00.run-*.json"), reverse=True)
    if all_runs:
        latest = json.loads(all_runs[0].read_text())
        if latest.get("builder", {}).get("triplets", 0) > 0:  # Has builder output
            e2e = {
                "file": all_runs[0].name,
                "triplets": latest["builder"]["triplets"],
                "grounded": f"{latest['query']['grounded_count']}/{latest['query']['total_questions']}",
            }
    
    print()
    print("=" * 80)
    print(f"RUN STATUS CHECK — {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 80)
    
    if studies:
        print("\nAblation Suite Progress:")
        for sid, info in studies.items():
            print(f"  {sid}: {info['file']:<40} grounded={info['grounded']:<8} faith={info['faith']}")
    else:
        print("\n  Ablation suite: not yet started")
    
    if e2e:
        print(f"\nFull E2E Run:")
        print(f"  {e2e['file']:<40} triplets={e2e['triplets']:<4} grounded={e2e['grounded']}")
    else:
        print("\n  Full E2E: not yet completed")
    
    print()

if __name__ == "__main__":
    check_runs()
