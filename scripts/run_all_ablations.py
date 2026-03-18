"""Automated ablation study runner with RAGAS integration.

Runs all 20 ablation studies (AB-00 through AB-20) sequentially with:
- Conditional RAGAS evaluation (only for high-impact studies)
- Resume capability (via state.json)
- Dry-run mode for validation
- Single-study mode for targeted runs
- Resilient execution (continues on failure)

Usage:
    python scripts/run_all_ablations.py                    # Run all studies
    python scripts/run_all_ablations.py --dry-run          # Validate configuration
    python scripts/run_all_ablations.py --study AB-05      # Run single study
    python scripts/run_all_ablations.py --resume           # Resume from last state
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path

# ── Repo root on path ──────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

# ── Load .env ─────────────────────────────────────────────────────────────────
from dotenv import load_dotenv  # type: ignore[import]

load_dotenv(ROOT / ".env")

# ── Notebook-style logging ─────────────────────────────────────────────────────
from src.config.llm_factory import reconfigure_from_env  # noqa: E402
from src.config.logging import setup_notebook_logging  # noqa: E402

reconfigure_from_env()
setup_notebook_logging()

# ── Import after setup ─────────────────────────────────────────────────────────
from src.evaluation.ablation_runner import ABLATION_MATRIX  # noqa: E402

logger = logging.getLogger("run_all_ablations")

# ── Configuration ───────────────────────────────────────────────────────────────

RESULTS_DIR = ROOT / "notebooks" / "ablation_results"
STATE_FILE = RESULTS_DIR / "ablation_state.json"

# Studies with RAGAS enabled (high impact on metrics)
RAGAS_ENABLED_STUDIES = {
    "AB-00",  # Baseline reference
    "AB-01",
    "AB-02",  # Retrieval mode variations
    "AB-03",  # Reranker OFF
    "AB-06",
    "AB-07",
    "AB-08",  # Chunking strategies
    "AB-15",  # Schema enrichment OFF
    "AB-16",  # Critic validation OFF
    "AB-19",  # Cypher healing OFF
}

# ── Utilities ──────────────────────────────────────────────────────────────────


def sep(char: str = "─", n: int = 60) -> str:
    return char * n


def print_header(title: str) -> None:
    print()
    print(sep("═"))
    print(f"  {title}")
    print(sep("═"))


def print_study_header(study_id: str, description: str) -> None:
    print()
    print(sep("─"))
    print(f"  {study_id}: {description}")
    print(sep("─"))


# ── State management ───────────────────────────────────────────────────────────


def load_state() -> dict[str, str | list[str]]:
    """Load the ablation state file."""
    if STATE_FILE.exists():
        with STATE_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)
    return {"completed": [], "failed": [], "start_time": datetime.now(tz=UTC).isoformat()}


def save_state(state: dict[str, str | list[str]]) -> None:
    """Save the ablation state file."""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with STATE_FILE.open("w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


def is_completed(study_id: str, state: dict[str, str | list[str]]) -> bool:
    """Check if a study has already completed."""
    return study_id in state.get("completed", [])


# ── Study execution ───────────────────────────────────────────────────────────


def _get_env_overrides(study_id: str) -> dict[str, str]:
    """Get environment overrides for a study."""
    config = ABLATION_MATRIX.get(study_id, {})
    return config.get("env_overrides", {})


def run_study(study_id: str, dry_run: bool = False) -> dict[str, object]:
    """Run a single ablation study.

    Args:
        study_id: The experiment ID (e.g., "AB-00").
        dry_run: If True, print configuration without executing.

    Returns:
        A dict with the study results.
    """
    if study_id not in ABLATION_MATRIX:
        raise ValueError(f"Unknown study: {study_id}")

    config = ABLATION_MATRIX[study_id]
    description = config["description"]
    env_overrides = config.get("env_overrides", {})
    run_ragas = config.get("run_ragas", False)

    print_study_header(study_id, description)
    print(f"  Env overrides: {env_overrides if env_overrides else '(none)'}")
    print(f"  Run RAGAS:     {run_ragas}")

    if dry_run:
        print(f"  [DRY RUN] Would execute {study_id}")
        return {
            "study_id": study_id,
            "dry_run": True,
            "env_overrides": env_overrides,
            "run_ragas": run_ragas,
        }

    # Build the command to run the study
    cmd = [
        sys.executable,
        "-c",
        f"""
import os
import sys
from pathlib import Path

# Set environment overrides
overrides = {json.dumps(env_overrides)}
for k, v in overrides.items():
    os.environ[k] = v

# Add repo to path
sys.path.insert(0, "{ROOT}")

# Reconfigure settings after env changes
from src.config.llm_factory import reconfigure_from_env
reconfigure_from_env()

# Import and run
from src.evaluation.ablation_runner import run_ablation

dataset_path = Path("{ROOT}") / "tests" / "fixtures" / "gold_standard.json"
result = run_ablation("{study_id}", dataset_path=dataset_path, run_ragas={run_ragas})

# Return as JSON
import json
print(json.dumps({{"result": "success", "metrics": result}}))
""",
    ]

    # Set up environment for the subprocess
    env = os.environ.copy()
    env.update(env_overrides)

    # Run the study
    log_file = RESULTS_DIR / f"{study_id}.log"

    start_time = time.time()

    try:
        with log_file.open("w", encoding="utf-8") as logf:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                env=env,
            )

            # Stream output to both console and log file
            for line in process.stdout:
                print(line, end="")
                logf.write(line)

            process.wait()
            elapsed = time.time() - start_time

            if process.returncode != 0:
                raise RuntimeError(f"Study failed with exit code {process.returncode}")

        # After successful completion, try to extract metrics from pipeline_run.py style execution
        # We'll use the pipeline_run.py approach instead for better control

        print(f"\n  Elapsed: {elapsed:.1f}s")

        return {
            "study_id": study_id,
            "success": True,
            "elapsed_s": round(elapsed, 1),
            "env_overrides": env_overrides,
            "run_ragas": run_ragas,
        }

    except Exception as exc:
        elapsed = time.time() - start_time
        logger.error("Study %s failed: %s", study_id, exc)
        return {
            "study_id": study_id,
            "success": False,
            "error": str(exc),
            "elapsed_s": round(elapsed, 1),
            "env_overrides": env_overrides,
            "run_ragas": run_ragas,
        }


def run_study_inline(study_id: str) -> dict[str, object]:
    """Run a single ablation study inline (not via subprocess).

    This is the preferred method for better control and output handling.
    Logs are written to both console and study-specific log file.
    """
    if study_id not in ABLATION_MATRIX:
        raise ValueError(f"Unknown study: {study_id}")

    config = ABLATION_MATRIX[study_id]
    description = config["description"]
    env_overrides = config.get("env_overrides", {})
    run_ragas = config.get("run_ragas", False)

    print_study_header(study_id, description)
    print(f"  Env overrides: {env_overrides if env_overrides else '(none)'}")
    print(f"  Run RAGAS:     {run_ragas}")

    # Set up file handler for this study's log
    log_file = RESULTS_DIR / f"{study_id}.log"
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    # Add file handler to root logger to capture all logs
    import logging

    file_handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        "%(asctime)s  %(name)-30s %(levelname)-8s %(message)s", datefmt="%H:%M:%S"
    )
    file_handler.setFormatter(file_formatter)

    # Add handler to all existing loggers
    root_logger = logging.getLogger()
    original_handlers = root_logger.handlers.copy()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    root_handler = logging.StreamHandler()
    root_handler.setLevel(logging.INFO)
    root_handler.setFormatter(file_formatter)
    root_logger.addHandler(root_handler)
    root_logger.addHandler(file_handler)

    start_time = time.time()
    result = None

    try:
        # Apply environment overrides
        saved_env = {k: os.environ.get(k) for k in env_overrides}
        try:
            for k, v in env_overrides.items():
                os.environ[k] = v
            reconfigure_from_env()

            # Import and run the ablation
            from src.evaluation.ablation_runner import run_ablation

            dataset_path = ROOT / "tests" / "fixtures" / "gold_standard.json"

            metrics = run_ablation(study_id, dataset_path=dataset_path, run_ragas=run_ragas)

            elapsed = time.time() - start_time

            result = {
                "study_id": study_id,
                "success": True,
                "elapsed_s": round(elapsed, 1),
                "metrics": metrics,
                "env_overrides": env_overrides,
                "run_ragas": run_ragas,
                "timestamp": datetime.now(tz=UTC).isoformat(),
            }

            # Save JSON result
            json_file = RESULTS_DIR / f"{study_id}.json"
            with json_file.open("w", encoding="utf-8") as f:
                json.dump(result, f, indent=2)

            print(f"\n  Result saved to: {json_file}")
            print(f"  Log saved to:    {log_file}")
            print(f"  Elapsed: {elapsed:.1f}s")

            if metrics:
                print(f"  Metrics: {metrics}")

        finally:
            # Restore environment
            for k, v in saved_env.items():
                if v is None:
                    os.environ.pop(k, None)
                else:
                    os.environ[k] = v
            reconfigure_from_env()

    except Exception as exc:
        elapsed = time.time() - start_time
        logger.error("Study %s failed: %s", study_id, exc)
        result = {
            "study_id": study_id,
            "success": False,
            "error": str(exc),
            "elapsed_s": round(elapsed, 1),
            "env_overrides": env_overrides,
            "run_ragas": run_ragas,
            "timestamp": datetime.now(tz=UTC).isoformat(),
        }
    finally:
        # Restore original handlers
        root_logger.removeHandler(root_handler)
        root_logger.removeHandler(file_handler)
        file_handler.close()
        for handler in original_handlers:
            root_logger.addHandler(handler)

    return result


# ── Main orchestration ─────────────────────────────────────────────────────────


def run_all_studies(
    dry_run: bool = False,
    resume: bool = False,
    single_study: str | None = None,
) -> dict[str, object]:
    """Run all or a subset of ablation studies.

    Args:
        dry_run: If True, print configuration without executing.
        resume: If True, skip studies that have already completed.
        single_study: If provided, run only this study.

    Returns:
        A summary dict with all results.
    """
    print_header("Ablation Study Runner")

    # Load state
    state = load_state()
    completed = state.get("completed", [])
    failed = state.get("failed", [])

    if resume and completed:
        print(f"  Resuming from state: {len(completed)} completed, {len(failed)} failed")

    # Determine which studies to run
    studies_to_run = [single_study] if single_study else sorted(ABLATION_MATRIX.keys())

    # Filter out completed studies if resuming
    if resume and not single_study:
        studies_to_run = [s for s in studies_to_run if s not in completed]

    print(f"  Studies to run: {len(studies_to_run)}")
    if studies_to_run:
        print(f"  {', '.join(studies_to_run)}")
    print()

    results: dict[str, dict[str, object]] = {}
    total_start = time.time()

    for i, study_id in enumerate(studies_to_run, 1):
        print(f"\n[{i}/{len(studies_to_run)}] Running {study_id}...")

        try:
            if dry_run:
                result = run_study(study_id, dry_run=True)
                results[study_id] = result
            else:
                result = run_study_inline(study_id)

                # Update state
                if result.get("success", False):
                    if study_id not in completed:
                        completed.append(study_id)
                else:
                    if study_id not in failed:
                        failed.append(study_id)

                state["completed"] = completed
                state["failed"] = failed
                state["last_update"] = datetime.now(tz=UTC).isoformat()
                save_state(state)

                results[study_id] = result

        except Exception as exc:
            logger.error("Unexpected error running %s: %s", study_id, exc)
            results[study_id] = {
                "study_id": study_id,
                "success": False,
                "error": f"Unexpected error: {exc}",
            }
            # Continue to next study

    total_elapsed = time.time() - total_start

    # Print summary
    print_header("Summary")
    successful = sum(1 for r in results.values() if r.get("success", False))
    print(f"  Total studies:  {len(results)}")
    print(f"  Successful:     {successful}")
    print(f"  Failed:         {len(results) - successful}")
    print(f"  Total elapsed:  {total_elapsed:.1f}s ({total_elapsed / 60:.1f}m)")

    print("\n  Study Results:")
    for study_id in sorted(results.keys()):
        r = results[study_id]
        status = "✅" if r.get("success", False) else "❌"
        elapsed = r.get("elapsed_s", "N/A")
        print(f"    {status} {study_id}: {elapsed}s")

    # Save final summary
    summary_file = RESULTS_DIR / "ablation_summary.json"
    with summary_file.open("w", encoding="utf-8") as f:
        json.dump(
            {
                "timestamp": datetime.now(tz=UTC).isoformat(),
                "total_elapsed_s": round(total_elapsed, 1),
                "studies": results,
                "state": state,
            },
            f,
            indent=2,
        )
    print(f"\n  Summary saved to: {summary_file}")

    return {
        "results": results,
        "state": state,
        "total_elapsed_s": total_elapsed,
    }


# ── CLI ─────────────────────────────────────────────────────────────────────────


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Automated ablation study runner with RAGAS integration"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print configuration without executing",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Resume from last state (skip completed studies)",
    )
    parser.add_argument(
        "--study",
        type=str,
        metavar="AB-XX",
        help="Run a single study (e.g., AB-05)",
    )
    args = parser.parse_args()

    # Validate study ID if provided
    if args.study and args.study not in ABLATION_MATRIX:
        print(f"Error: Unknown study '{args.study}'")
        print(f"Available studies: {', '.join(sorted(ABLATION_MATRIX.keys()))}")
        sys.exit(1)

    # Run the studies
    run_all_studies(
        dry_run=args.dry_run,
        resume=args.resume,
        single_study=args.study,
    )


if __name__ == "__main__":
    main()
