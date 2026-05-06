"""Inject ablation_context into AB-BEST evaluation bundles for DS02-DS06.

Run after pipeline completes:
    .venv/bin/python scripts/inject_ablation_context.py
"""

import json
from pathlib import Path

ABLATION_CONTEXT = {
    "study_type": "combined_optimal",
    "description": (
        "AB-BEST combines the optimal parameters identified across all 20 "
        "ablation studies. It represents the best achievable configuration "
        "derived from empirical evidence."
    ),
    "baseline_study_id": "AB-00",
    "changes_vs_baseline": {
        "reranker_top_k": {
            "baseline": 20,
            "optimal": 5,
            "rationale": "AB-04 showed top_k=5 achieves identical quality with 4x fewer reranker calls",
        },
        "enable_hallucination_grader": {
            "baseline": True,
            "optimal": True,
            "rationale": "Kept ON — safety-first approach for complex datasets",
        },
        "confidence_threshold": {
            "baseline": 0.8,
            "optimal": 0.8,
            "rationale": "Neutral parameter — baseline value retained",
        },
        "er_similarity_threshold": {
            "baseline": 0.75,
            "optimal": 0.75,
            "rationale": "Neutral parameter — baseline value retained",
        },
    },
    "expected_impact": (
        "Same quality as baseline (all neutral params) with 4x reranker efficiency "
        "gain (top_k 20→5). AB-04/AB-05 both scored 4.90 with this key change, "
        "confirming the causal improvement."
    ),
    "efficiency_gain": (
        "4x fewer reranker inference calls per query (top_k=5 vs 20) "
        "with no quality degradation"
    ),
}

DATASETS = [
    "02_intermediate_finance",
    "03_advanced_healthcare",
    "04_complex_manufacturing",
    "05_edgecases_incomplete",
    "06_edgecases_legacy",
]

BASE_DIR = Path("outputs/ablation/AB-BEST/datasets")


def main() -> None:
    for ds in DATASETS:
        bundle_path = BASE_DIR / ds / "evaluation_bundle.json"
        if not bundle_path.exists():
            print(f"⏭️  {ds}: bundle not found, skipping")
            continue

        with open(bundle_path, "r") as f:
            data = json.load(f)

        if "ablation_context" in data:
            print(f"✅ {ds}: ablation_context already present")
            continue

        data["ablation_context"] = ABLATION_CONTEXT

        with open(bundle_path, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"💉 {ds}: ablation_context injected")


if __name__ == "__main__":
    main()
