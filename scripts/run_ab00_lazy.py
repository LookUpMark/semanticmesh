#!/usr/bin/env python
"""Run AB-00 with lazy extraction to bypass LM Studio requirement."""

import os
import sys
from pathlib import Path

# Enable lazy extraction BEFORE importing anything else
os.environ["USE_LAZY_EXTRACTION"] = "true"

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.evaluation.ablation_runner import run_ablation

if __name__ == "__main__":
    print("=" * 70)
    print("AB-00 ABLATION STUDY - LAZY EXTRACTION MODE")
    print("=" * 70)
    print()
    print("Configuration:")
    print("  - Lazy extraction: ENABLED (bypasses LM Studio)")
    print("  - Debug trace: ENABLED")
    print("  - Dataset: 01_basics_ecommerce")
    print("  - RAGAS: ENABLED")
    print()

    # Run AB-00 with debug trace
    metrics = run_ablation(
        experiment_id="AB-00",
        dataset_path=Path("tests/fixtures/01_basics_ecommerce/gold_standard.json"),
        run_ragas=True,
        debug_trace=True,
    )

    print()
    print("=" * 70)
    print("RESULTS SUMMARY")
    print("=" * 70)
    for key, value in metrics.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.4f}")
        else:
            print(f"  {key}: {value}")
