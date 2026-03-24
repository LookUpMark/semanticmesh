#!/usr/bin/env python
"""Helper script to run AB-00 with full debug tracing enabled.

This script executes the AB-00 ablation study with detailed tracing
to capture the complete data flow through the pipeline.

Usage:
    python scripts/run_ab00_debug.py [--dataset PATH] [--max-samples N]

Examples:
    # Run with default 01_basics_ecommerce dataset
    python scripts/run_ab00_debug.py

    # Run with custom dataset
    python scripts/run_ab00_debug.py --dataset tests/fixtures/02_intermediate_finance/gold_standard.json

    # Run with limited samples for faster testing
    python scripts/run_ab00_debug.py --max-samples 5
"""

from __future__ import annotations

import argparse
from pathlib import Path

from src.config.settings import get_settings
from src.evaluation.ablation_runner import run_ablation


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Run AB-00 ablation study with full debug tracing"
    )
    parser.add_argument(
        "--dataset",
        type=Path,
        default=Path("tests/fixtures/01_basics_ecommerce/gold_standard.json"),
        help="Path to gold standard dataset (default: 01_basics_ecommerce)",
    )
    parser.add_argument(
        "--max-samples",
        type=int,
        default=None,
        help="Limit evaluation to N samples (faster for testing)",
    )
    parser.add_argument(
        "--ragas",
        action="store_true",
        help="Enable RAGAS evaluation (default: pipeline metrics only)",
    )
    parser.add_argument(
        "--no-builder",
        action="store_true",
        help="Skip builder and only run query evaluation (requires existing graph)",
    )

    args = parser.parse_args()

    # Verify dataset exists
    if not args.dataset.exists():
        print(f"❌ Error: Dataset not found: {args.dataset}")
        print(f"   Available datasets:")
        for d in Path("tests/fixtures").glob("*/gold_standard.json"):
            print(f"     - {d}")
        return

    print("=" * 60)
    print("🔬 AB-00 Debug Trace Run")
    print("=" * 60)
    print(f"📁 Dataset: {args.dataset}")
    print(f"📊 Max samples: {args.max_samples or 'All'}")
    print(f"🧪 RAGAS: {'Enabled' if args.ragas else 'Disabled (pipeline metrics only)'}")
    print(f"📦 Debug trace: Enabled")
    print()

    # Set trace output directory
    settings = get_settings()
    trace_dir = Path(settings.trace_output_dir) / "AB-00"
    trace_dir.mkdir(parents=True, exist_ok=True)

    print(f"💾 Traces will be saved to: {trace_dir}")
    print()

    # Run AB-00 with debug tracing
    try:
        metrics = run_ablation(
            experiment_id="AB-00",
            dataset_path=args.dataset,
            run_ragas=args.ragas,
            debug_trace=True,
        )

        print()
        print("=" * 60)
        print("✅ AB-00 Debug Run Complete")
        print("=" * 60)
        print(f"\n📊 Metrics:")
        for key, value in metrics.items():
            if isinstance(value, float):
                print(f"   {key}: {value:.4f}")
            else:
                print(f"   {key}: {value}")

        print(f"\n💾 Trace files saved to: {trace_dir}")
        print(f"\n📖 To analyze traces, run:")
        print(f"   python scripts/analyze_ab00_trace.py {trace_dir}")

    except Exception as e:
        print(f"\n❌ Error during AB-00 run: {e}")
        raise


if __name__ == "__main__":
    main()
