#!/usr/bin/env python3
"""Overnight ablation campaign — runs AB-01 through AB-20 across all datasets.

Execution strategy
──────────────────
  • Query-only ablations (retrieval mode, reranker, grader):
    The baseline graph is rebuilt ONCE per dataset, then each query-only
    variant runs with --no-builder (reuses the existing graph).

  • Builder ablations (chunking, ER, enrichment, healing, critic):
    Each study × dataset combination runs the FULL pipeline (builder + query).

Studies are executed in priority order so that the highest-impact experiments
finish first.  If the process is interrupted (Ctrl-C), it finishes the current
run and prints a summary of what completed.

Usage
─────
    # Full campaign (all 20 studies × 6 datasets)
    python scripts/run_overnight_ablations.py

    # Dry run — preview what would execute
    python scripts/run_overnight_ablations.py --dry-run

    # Only the 9 high-impact studies (with RAGAS evaluation)
    python scripts/run_overnight_ablations.py --high-impact-only

    # Specific studies
    python scripts/run_overnight_ablations.py --studies AB-01 AB-02 AB-03

    # Resume after interruption — skip runs that already have results
    python scripts/run_overnight_ablations.py --skip-completed

    # Combine options
    python scripts/run_overnight_ablations.py --high-impact-only --skip-completed --run-tag v5
"""

from __future__ import annotations

import argparse
import json
import os
import signal
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# ── Paths ────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parents[1]
FIXTURES_DIR = ROOT / "tests" / "fixtures"
RESULTS_DIR = ROOT / "notebooks" / "ablation" / "ablation_results"

# ── Datasets ─────────────────────────────────────────────────────────────────
DATASETS = [
    "01_basics_ecommerce",
    "02_intermediate_finance",
    "03_advanced_healthcare",
    "04_complex_manufacturing",
    "05_edgecases_incomplete",
    "06_edgecases_legacy",
]

# ── Study definitions ────────────────────────────────────────────────────────
# Each study maps to env-var overrides taken from ABLATION_MATRIX.
#
# NOTE — AB-15 is INVERTED: the baseline already runs with enrichment OFF
# (enable_schema_enrichment=False), so this ablation tests enrichment ON
# to measure whether it adds value.
# ─────────────────────────────────────────────────────────────────────────────

STUDIES: dict[str, dict] = {
    "AB-01": {
        "desc": "Vector-only retrieval (no BM25, no graph traversal)",
        "env": {"RETRIEVAL_MODE": "vector"},
        "query_only": True,
        "high_impact": True,
    },
    "AB-02": {
        "desc": "BM25-only retrieval (no vector, no graph traversal)",
        "env": {"RETRIEVAL_MODE": "bm25"},
        "query_only": True,
        "high_impact": True,
    },
    "AB-03": {
        "desc": "Reranker OFF — raw hybrid pool ranking",
        "env": {"ENABLE_RERANKER": "false"},
        "query_only": True,
        "high_impact": True,
    },
    "AB-04": {
        "desc": "Reranker top_k=5 — smaller reranking pool",
        "env": {"RERANKER_TOP_K": "5"},
        "query_only": True,
        "high_impact": False,
    },
    "AB-05": {
        "desc": "Reranker top_k=20 — larger reranking pool",
        "env": {"RERANKER_TOP_K": "20"},
        "query_only": True,
        "high_impact": False,
    },
    "AB-06": {
        "desc": "Chunking 128/16 — smaller chunks",
        "env": {"CHUNK_SIZE": "128", "CHUNK_OVERLAP": "16"},
        "query_only": False,
        "high_impact": True,
    },
    "AB-07": {
        "desc": "Chunking 384/48 — larger chunks",
        "env": {"CHUNK_SIZE": "384", "CHUNK_OVERLAP": "48"},
        "query_only": False,
        "high_impact": True,
    },
    "AB-08": {
        "desc": "Chunking 512/64 — largest chunks",
        "env": {"CHUNK_SIZE": "512", "CHUNK_OVERLAP": "64"},
        "query_only": False,
        "high_impact": True,
    },
    "AB-09": {
        "desc": "Extraction max_tokens=4096 — conservative limit",
        "env": {"LLM_MAX_TOKENS_EXTRACTION": "4096"},
        "query_only": False,
        "high_impact": False,
    },
    "AB-10": {
        "desc": "Extraction max_tokens=16384 — generous limit",
        "env": {"LLM_MAX_TOKENS_EXTRACTION": "16384"},
        "query_only": False,
        "high_impact": False,
    },
    "AB-11": {
        "desc": "ER similarity threshold=0.65 — aggressive merging",
        "env": {"ER_SIMILARITY_THRESHOLD": "0.65"},
        "query_only": False,
        "high_impact": False,
    },
    "AB-12": {
        "desc": "ER similarity threshold=0.85 — conservative merging",
        "env": {"ER_SIMILARITY_THRESHOLD": "0.85"},
        "query_only": False,
        "high_impact": False,
    },
    "AB-13": {
        "desc": "ER blocking top_k=5 — smaller candidate set",
        "env": {"ER_BLOCKING_TOP_K": "5"},
        "query_only": False,
        "high_impact": False,
    },
    "AB-14": {
        "desc": "ER blocking top_k=20 — larger candidate set",
        "env": {"ER_BLOCKING_TOP_K": "20"},
        "query_only": False,
        "high_impact": False,
    },
    "AB-15": {
        "desc": "Schema enrichment ON (inverted — baseline has enrichment OFF)",
        "env": {"ENABLE_SCHEMA_ENRICHMENT": "true"},
        "query_only": False,
        "high_impact": True,
    },
    "AB-16": {
        "desc": "Actor-Critic validation OFF — accept all mapping proposals",
        "env": {"ENABLE_CRITIC_VALIDATION": "false"},
        "query_only": False,
        "high_impact": True,
    },
    "AB-17": {
        "desc": "Confidence threshold=0.70 — more HITL interrupts",
        "env": {"CONFIDENCE_THRESHOLD": "0.70"},
        "query_only": False,
        "high_impact": False,
    },
    "AB-18": {
        "desc": "Confidence threshold=0.85 — fewer HITL interrupts",
        "env": {"CONFIDENCE_THRESHOLD": "0.85"},
        "query_only": False,
        "high_impact": False,
    },
    "AB-19": {
        "desc": "Cypher healing OFF — immediate fail on syntax error",
        "env": {"ENABLE_CYPHER_HEALING": "false"},
        "query_only": False,
        "high_impact": True,
    },
    "AB-20": {
        "desc": "Hallucination grader OFF — return first answer without grading",
        "env": {"ENABLE_HALLUCINATION_GRADER": "false"},
        "query_only": True,
        "high_impact": False,
    },
}

# Execution order — highest-impact studies first so the most important
# experiments finish even if the campaign is interrupted mid-way.
PRIORITY_ORDER = [
    # P1: Retrieval architecture (query-only, high impact)
    "AB-01", "AB-02", "AB-03",
    # P2: Critical builder components (high impact)
    "AB-19", "AB-16",
    # P3: Hallucination grader (query-only)
    "AB-20",
    # P4: Chunking variations (builder, high impact)
    "AB-06", "AB-07", "AB-08",
    # P5: Schema enrichment ON (inverted, high impact)
    "AB-15",
    # P6: Reranker top_k tuning (query-only)
    "AB-04", "AB-05",
    # P7: Extraction & ER tuning (builder)
    "AB-09", "AB-10", "AB-11", "AB-12", "AB-13", "AB-14",
    # P8: Confidence threshold tuning (builder)
    "AB-17", "AB-18",
]


# ── Signal handling for graceful stop ────────────────────────────────────────
_stop_requested = False


def _handle_signal(signum, frame):  # noqa: ANN001, ARG001
    global _stop_requested  # noqa: PLW0603
    _stop_requested = True
    print(
        "\n⚠  Graceful stop requested — finishing current run, then stopping.\n",
        flush=True,
    )


signal.signal(signal.SIGINT, _handle_signal)
signal.signal(signal.SIGTERM, _handle_signal)


# ── Helpers ──────────────────────────────────────────────────────────────────
def _is_completed(study_id: str, dataset_id: str) -> bool:
    """Return True if run.json already exists for this study/dataset."""
    return (RESULTS_DIR / study_id / dataset_id / "run.json").exists()


def _fmt(seconds: float) -> str:
    """Format seconds as HH:MM:SS."""
    h, rem = divmod(int(seconds), 3600)
    m, s = divmod(rem, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


def _run_ab00(
    study_id: str,
    dataset_id: str,
    *,
    no_builder: bool = False,
    env_overrides: dict[str, str] | None = None,
    run_tag: str = "ablation",
    max_samples: int | None = None,
    log_path: Path | None = None,
    timeout: int = 2400,
) -> tuple[bool, float]:
    """Spawn ``run_ab00.py`` as a subprocess.

    Returns (success, elapsed_seconds).
    """
    dataset_path = FIXTURES_DIR / dataset_id / "gold_standard.json"

    cmd = [
        sys.executable,
        str(ROOT / "scripts" / "run_ab00.py"),
        "--dataset", str(dataset_path),
        "--study-id", study_id,
        "--run-tag", run_tag,
    ]
    if no_builder:
        cmd.append("--no-builder")
    if max_samples is not None:
        cmd.extend(["--max-samples", str(max_samples)])

    env = os.environ.copy()
    if env_overrides:
        env.update(env_overrides)

    # Redirect subprocess output to the campaign log (keeps terminal clean)
    stdout_target = subprocess.DEVNULL
    if log_path is not None:
        log_path.parent.mkdir(parents=True, exist_ok=True)

    t0 = time.time()
    try:
        if log_path is not None:
            with open(log_path, "a") as flog:
                flog.write(f"\n{'='*70}\n")
                flog.write(f"  {study_id} / {dataset_id}\n")
                flog.write(f"  cmd: {' '.join(cmd)}\n")
                flog.write(f"  env overrides: {env_overrides or {}}\n")
                flog.write(f"{'='*70}\n\n")
                flog.flush()
                proc = subprocess.run(
                    cmd, env=env, cwd=str(ROOT),
                    stdout=flog, stderr=subprocess.STDOUT,
                    timeout=timeout,
                )
        else:
            proc = subprocess.run(
                cmd, env=env, cwd=str(ROOT),
                stdout=stdout_target, stderr=subprocess.STDOUT,
                timeout=timeout,
            )
        elapsed = time.time() - t0
        return proc.returncode == 0, elapsed

    except subprocess.TimeoutExpired:
        elapsed = time.time() - t0
        print(f"    ⚠ TIMEOUT after {_fmt(elapsed)}", flush=True)
        return False, elapsed
    except Exception as exc:
        elapsed = time.time() - t0
        print(f"    ⚠ ERROR: {exc}", flush=True)
        return False, elapsed


# ── Campaign orchestration ───────────────────────────────────────────────────
def run_campaign(
    studies: list[str],
    datasets: list[str],
    *,
    dry_run: bool = False,
    skip_completed: bool = False,
    run_tag: str = "ablation",
    log_path: Path | None = None,
) -> dict[str, dict]:
    """Execute the full ablation campaign.

    Returns mapping ``"STUDY/DATASET" -> {"status": str, "elapsed": float}``.
    """
    global _stop_requested  # noqa: PLW0603
    results: dict[str, dict] = {}
    campaign_t0 = time.time()

    # Split studies into query-only vs builder (preserving priority order)
    query_only = [s for s in studies if STUDIES[s]["query_only"]]
    builder = [s for s in studies if not STUDIES[s]["query_only"]]

    # Estimate total subprocess invocations
    total_runs = 0
    if query_only:
        total_runs += len(datasets) * (1 + len(query_only))   # rebuild + N queries
    if builder:
        total_runs += len(datasets) * len(builder)
    run_idx = 0

    # ── Phase 1: Query-only ablations ────────────────────────────────────
    if query_only:
        print(flush=True)
        print("━" * 70, flush=True)
        _n = len(query_only)
        print(
            f"  PHASE 1 — Query-only ablations  ({_n} studies × {len(datasets)} datasets)",
            flush=True,
        )
        print(f"  Studies: {', '.join(query_only)}", flush=True)
        print("━" * 70, flush=True)

        for ds_i, ds in enumerate(datasets, 1):
            if _stop_requested:
                break

            print(f"\n{'─'*60}", flush=True)
            print(f"  📂 Dataset {ds_i}/{len(datasets)}: {ds}", flush=True)
            print(f"{'─'*60}", flush=True)

            # --- 1a. Rebuild baseline graph for this dataset ----------------
            run_idx += 1
            print(
                f"\n  [{run_idx}/{total_runs}] Rebuilding baseline graph …",
                flush=True,
            )
            if not dry_run:
                ok, elapsed = _run_ab00(
                    "_REBUILD", ds,
                    no_builder=False,
                    run_tag=f"{run_tag}-rebuild",
                    max_samples=1,
                    log_path=log_path,
                    timeout=1800,
                )
                if ok:
                    print(f"           ✓ graph ready  ({_fmt(elapsed)})", flush=True)
                else:
                    print(f"           ✗ rebuild FAILED ({_fmt(elapsed)})", flush=True)
                    print(
                        "           Skipping all query-only ablations for this dataset.",
                        flush=True,
                    )
                    for s in query_only:
                        run_idx += 1
                        results[f"{s}/{ds}"] = {"status": "SKIP-DEP", "elapsed": 0}
                    continue
            else:
                print("           [dry-run] would rebuild baseline graph", flush=True)

            # --- 1b. Run each query-only study with --no-builder ------------
            for study_id in query_only:
                if _stop_requested:
                    break

                run_idx += 1
                key = f"{study_id}/{ds}"

                if skip_completed and _is_completed(study_id, ds):
                    print(f"\n  [{run_idx}/{total_runs}] {key} — SKIP (results exist)", flush=True)
                    results[key] = {"status": "SKIP", "elapsed": 0}
                    continue

                info = STUDIES[study_id]
                print(
                    f"\n  [{run_idx}/{total_runs}] {study_id} — {info['desc']}",
                    flush=True,
                )
                print(f"           dataset={ds}  env={info['env']}", flush=True)

                if dry_run:
                    results[key] = {"status": "DRY", "elapsed": 0}
                    continue

                ok, elapsed = _run_ab00(
                    study_id, ds,
                    no_builder=True,
                    env_overrides=info["env"],
                    run_tag=run_tag,
                    log_path=log_path,
                )
                status = "OK" if ok else "FAIL"
                results[key] = {"status": status, "elapsed": elapsed}
                print(f"           → {status}  ({_fmt(elapsed)})", flush=True)

    # ── Phase 2: Builder ablations ───────────────────────────────────────
    if builder and not _stop_requested:
        print(flush=True)
        print("━" * 70, flush=True)
        _n = len(builder)
        print(
            f"  PHASE 2 — Builder ablations  ({_n} studies × {len(datasets)} datasets)",
            flush=True,
        )
        print(f"  Studies: {', '.join(builder)}", flush=True)
        print("━" * 70, flush=True)

        for study_id in builder:
            if _stop_requested:
                break

            info = STUDIES[study_id]
            print(f"\n{'─'*60}", flush=True)
            print(f"  🔧 {study_id} — {info['desc']}", flush=True)
            print(f"     env overrides: {info['env']}", flush=True)
            print(f"{'─'*60}", flush=True)

            for ds_i, ds in enumerate(datasets, 1):
                if _stop_requested:
                    break

                run_idx += 1
                key = f"{study_id}/{ds}"

                if skip_completed and _is_completed(study_id, ds):
                    print(
                        f"\n  [{run_idx}/{total_runs}] {key} — SKIP (results exist)",
                        flush=True,
                    )
                    results[key] = {"status": "SKIP", "elapsed": 0}
                    continue

                print(
                    f"\n  [{run_idx}/{total_runs}] {study_id} × {ds}  (full pipeline)",
                    flush=True,
                )

                if dry_run:
                    results[key] = {"status": "DRY", "elapsed": 0}
                    continue

                ok, elapsed = _run_ab00(
                    study_id, ds,
                    no_builder=False,
                    env_overrides=info["env"],
                    run_tag=run_tag,
                    log_path=log_path,
                )
                status = "OK" if ok else "FAIL"
                results[key] = {"status": status, "elapsed": elapsed}
                print(f"           → {status}  ({_fmt(elapsed)})", flush=True)

    # ── Final summary ────────────────────────────────────────────────────
    campaign_elapsed = time.time() - campaign_t0

    print(flush=True)
    print("━" * 70, flush=True)
    print("  CAMPAIGN COMPLETE", flush=True)
    print("━" * 70, flush=True)
    print(f"  Total elapsed : {_fmt(campaign_elapsed)}", flush=True)

    if _stop_requested:
        print("  ⚠  Stopped early (SIGINT/SIGTERM)", flush=True)

    ok_n = sum(1 for r in results.values() if r["status"] == "OK")
    fail_n = sum(1 for r in results.values() if r["status"] == "FAIL")
    skip_n = sum(1 for r in results.values() if r["status"] in ("SKIP", "SKIP-DEP"))

    print(f"  OK: {ok_n}  |  FAIL: {fail_n}  |  SKIP: {skip_n}", flush=True)

    # List failures
    if fail_n:
        print("\n  ✗ Failed runs:", flush=True)
        for key, r in results.items():
            if r["status"] == "FAIL":
                print(f"      {key}  ({_fmt(r['elapsed'])})", flush=True)

    # Per-study summary table
    if ok_n:
        print("\n  Per-study results:", flush=True)
        print(
            f"  {'Study':<8} {'DS01':>4} {'DS02':>4} {'DS03':>4}"
            f" {'DS04':>4} {'DS05':>4} {'DS06':>4}  Elapsed",
            flush=True,
        )
        print(f"  {'─'*8} {'─'*4} {'─'*4} {'─'*4} {'─'*4} {'─'*4} {'─'*4}  {'─'*8}", flush=True)

        for study_id in studies:
            cells = []
            total_elapsed = 0.0
            for ds in datasets:
                r = results.get(f"{study_id}/{ds}", {})
                st = r.get("status", "—")
                total_elapsed += r.get("elapsed", 0)
                if st == "OK":
                    cells.append("  ✓ ")
                elif st == "FAIL":
                    cells.append("  ✗ ")
                elif st in ("SKIP", "SKIP-DEP"):
                    cells.append("  · ")
                else:
                    cells.append("  — ")
            any_result = any(
                results.get(f"{study_id}/{ds}", {}).get("status") in ("OK", "FAIL")
                for ds in datasets
            )
            if any_result:
                row = "".join(cells)
                print(f"  {study_id:<8}{row}  {_fmt(total_elapsed)}", flush=True)

    return results


# ── CLI ──────────────────────────────────────────────────────────────────────
def main() -> None:
    parser = argparse.ArgumentParser(
        description="Overnight ablation campaign runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Preview execution plan without running anything",
    )
    parser.add_argument(
        "--studies", nargs="+", metavar="AB-XX",
        help="Run only these studies (e.g. --studies AB-01 AB-02 AB-03)",
    )
    parser.add_argument(
        "--high-impact-only", action="store_true",
        help="Only run the 9 high-impact studies (those with RAGAS evaluation)",
    )
    parser.add_argument(
        "--skip-completed", action="store_true",
        help="Skip study/dataset pairs that already have run.json",
    )
    parser.add_argument(
        "--run-tag", default="ablation",
        help="Run tag for output file naming (default: ablation)",
    )
    parser.add_argument(
        "--datasets", nargs="+", metavar="DS",
        help="Run only these datasets (e.g. --datasets 01_basics_ecommerce 03_advanced_healthcare)",
    )
    args = parser.parse_args()

    # ── Resolve study list ───────────────────────────────────────────────
    if args.studies:
        studies = args.studies
        for s in studies:
            if s not in STUDIES:
                parser.error(f"Unknown study '{s}'. Available: {', '.join(STUDIES)}")
    elif args.high_impact_only:
        studies = [s for s in PRIORITY_ORDER if STUDIES[s]["high_impact"]]
    else:
        studies = list(PRIORITY_ORDER)

    # ── Resolve dataset list ─────────────────────────────────────────────
    datasets = args.datasets if args.datasets else list(DATASETS)
    for ds in datasets:
        gs = FIXTURES_DIR / ds / "gold_standard.json"
        if not gs.exists():
            parser.error(f"Dataset not found: {gs}")

    # ── Print execution plan ─────────────────────────────────────────────
    qo = [s for s in studies if STUDIES[s]["query_only"]]
    bl = [s for s in studies if not STUDIES[s]["query_only"]]
    total_runs = len(datasets) * len(studies)
    if qo:
        total_runs += len(datasets)  # baseline rebuilds

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    print("=" * 70, flush=True)
    print("  ABLATION CAMPAIGN", flush=True)
    print(f"  Started : {now}", flush=True)
    print("=" * 70, flush=True)
    print(f"  Studies    : {len(studies)}  ({len(qo)} query-only, {len(bl)} builder)", flush=True)
    print(f"  Datasets   : {len(datasets)}", flush=True)
    print(f"  Total runs : ~{total_runs}", flush=True)
    print(f"  Run tag    : {args.run_tag}", flush=True)
    print(f"  Dry run    : {args.dry_run}", flush=True)
    print(f"  Skip done  : {args.skip_completed}", flush=True)
    print(flush=True)

    for s in studies:
        info = STUDIES[s]
        kind = "Q" if info["query_only"] else "B"
        star = "★" if info["high_impact"] else " "
        print(f"  {star} [{kind}] {s}: {info['desc']}", flush=True)

    print(flush=True)

    # ── Campaign log file ────────────────────────────────────────────────
    log_path: Path | None = None
    if not args.dry_run:
        log_path = RESULTS_DIR / f"campaign_{log_ts}.log"
        log_path.parent.mkdir(parents=True, exist_ok=True)
        print(f"  Campaign log: {log_path}", flush=True)

    # ── Execute ──────────────────────────────────────────────────────────
    results = run_campaign(
        studies=studies,
        datasets=datasets,
        dry_run=args.dry_run,
        skip_completed=args.skip_completed,
        run_tag=args.run_tag,
        log_path=log_path,
    )

    # ── Save campaign summary JSON ───────────────────────────────────────
    if not args.dry_run:
        summary_path = RESULTS_DIR / f"campaign_{log_ts}.json"
        summary = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "studies": studies,
            "datasets": datasets,
            "run_tag": args.run_tag,
            "high_impact_only": args.high_impact_only,
            "results": results,
        }
        summary_path.write_text(json.dumps(summary, indent=2, default=str))
        print(f"\n  Campaign summary : {summary_path}", flush=True)
        if log_path:
            print(f"  Campaign log     : {log_path}", flush=True)


if __name__ == "__main__":
    main()
