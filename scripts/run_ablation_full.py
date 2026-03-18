"""Automated ablation study runner - Full pipeline with RAGAS.

This script runs all 20 ablation studies (AB-00 through AB-20) sequentially,
following the same pattern as pipeline_run.py but with environment variable overrides
for each study.

Each study:
1. Clears the Neo4j graph
2. Runs the Builder Graph (triplet extraction, ER, mapping, Cypher upsert)
3. Runs the Query Graph with 4 test questions
4. Optionally runs RAGAS evaluation on the gold-standard dataset

Results are saved to notebooks/ablation_results/AB-XX.json and AB-XX.log
"""

from __future__ import annotations

import argparse
import json
import logging
import os
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

# ── Pipeline config (matches pipeline_run.py defaults) ────────────────────────────
os.environ.setdefault("NEO4J_URI", "bolt://localhost:7687")
os.environ.setdefault("NEO4J_USER", "neo4j")
os.environ.setdefault("NEO4J_PASSWORD", "test_password")
os.environ.setdefault("LLM_MODEL_REASONING", "openai/gpt-oss-120b:free")
os.environ.setdefault("LLM_MODEL_EXTRACTION", "openai/gpt-4.1-nano")
os.environ.setdefault("LLM_MAX_TOKENS_REASONING", "16384")
os.environ.setdefault("LLM_MAX_TOKENS_EXTRACTION", "16384")
os.environ.setdefault("EXTRACTION_CONCURRENCY", "10")  # Parallel extraction
os.environ.setdefault("ER_SIMILARITY_THRESHOLD", "0.75")
os.environ.setdefault("RETRIEVAL_VECTOR_TOP_K", "20")
os.environ.setdefault("RETRIEVAL_BM25_TOP_K", "10")
os.environ.setdefault("RERANKER_TOP_K", "10")
os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")

# ── Notebook-style logging ─────────────────────────────────────────────────────
from src.config.llm_factory import reconfigure_from_env  # noqa: E402
from src.config.logging import setup_notebook_logging  # noqa: E402

reconfigure_from_env()
setup_notebook_logging()

logger = logging.getLogger("ablation_runner")

# ── Data fixtures ─────────────────────────────────────────────────────────────
FIXTURE_DIR = ROOT / "tests" / "fixtures"
DOC_PATHS = [
    FIXTURE_DIR / "sample_docs" / "business_glossary.txt",
    FIXTURE_DIR / "sample_docs" / "data_dictionary.txt",
]
DDL_PATHS = [FIXTURE_DIR / "sample_ddl" / "complex_schema.sql"]

# ── Test questions (same as pipeline_run.py) ────────────────────────────────────
TEST_QUESTIONS = [
    "What entities exist in the business domain?",
    "Which table stores customer information?",
    "How are customers and orders related?",
    "What columns does the product table have?",
]

# ── Ablation matrix ───────────────────────────────────────────────────────────
from src.evaluation.ablation_runner import ABLATION_MATRIX  # noqa: E402

# ── Results directory ───────────────────────────────────────────────────────────
RESULTS_DIR = ROOT / "notebooks" / "ablation" / "ablation_results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


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


# ── Study execution ───────────────────────────────────────────────────────────


def run_ablation_study(
    study_id: str,
    run_ragas: bool = False,
) -> dict[str, object]:
    """Run a single ablation study with the full pipeline.

    Args:
        study_id: The experiment ID (e.g., "AB-00").
        run_ragas: Whether to run RAGAS evaluation after the query phase.

    Returns:
        A dict with the study results.
    """
    if study_id not in ABLATION_MATRIX:
        raise ValueError(f"Unknown study: {study_id}")

    config = ABLATION_MATRIX[study_id]
    description = config["description"]
    env_overrides = config.get("env_overrides", {})
    study_run_ragas = run_ragas and config.get("run_ragas", False)

    print_study_header(study_id, description)
    if env_overrides:
        print(f"  Env overrides: {env_overrides}")
    else:
        print("  Env overrides: (none - using defaults)")
    print(f"  Run RAGAS:     {study_run_ragas}")

    # Set up file logging for this study
    log_file = RESULTS_DIR / f"{study_id}.log"
    file_handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        "%(asctime)s  %(name)-30s %(levelname)-8s %(message)s", datefmt="%H:%M:%S"
    )
    file_handler.setFormatter(file_formatter)

    # Configure root logger
    root_logger = logging.getLogger()
    original_handlers = root_logger.handlers.copy()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(file_formatter)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

    start_time = time.time()
    result = None

    try:
        # Save and override environment
        saved_env = {k: os.environ.get(k) for k in env_overrides}
        try:
            # Apply environment overrides for this study
            for k, v in env_overrides.items():
                os.environ[k] = v
            reconfigure_from_env()

            # ── 1. Builder Graph ───────────────────────────────────────────────
            from src.graph.builder_graph import run_builder  # noqa: E402

            print("\n[1/2] Builder Graph …")
            t0 = time.time()
            state = run_builder(
                raw_documents=DOC_PATHS,
                ddl_paths=DDL_PATHS,
                production=False,
                clear_graph=True,
            )
            builder_elapsed = time.time() - t0

            triplets = state.get("triplets", [])
            entities = state.get("entities", [])
            tables = state.get("tables", [])
            enriched = state.get("enriched_tables", [])
            completed = state.get("completed_tables", [])
            failed = state.get("cypher_failed", False)

            print(f"\n    Elapsed         : {builder_elapsed:.1f} s")
            print(f"    Triplets        : {len(triplets)}")
            print(f"    Entities        : {len(entities)}")
            print(f"    Tables parsed   : {len(tables)}")
            print(f"    Tables enriched : {len(enriched)}")
            print(f"    Tables completed: {len(completed)} / {len(tables)}")
            print(f"    Cypher failed   : {failed}")

            # ── 2. Query Graph ─────────────────────────────────────────────────
            from src.generation.query_graph import run_query  # noqa: E402

            print("\n[2/2] Query Graph …")
            t1 = time.time()

            grounded_count = 0
            results = []
            for i, q in enumerate(TEST_QUESTIONS, 1):
                r = run_query(q)
                answer = r.get("final_answer", "")
                grounded = bool(
                    answer
                    and answer.strip()
                    and not answer.strip().lower().startswith("i cannot")
                    and not answer.strip().lower().startswith("i don't")
                )
                grounded_count += int(grounded)
                mark = "✅" if grounded else "❌"
                results.append((q, answer, grounded))
                print(f"\n    [{i}/{len(TEST_QUESTIONS)}] {mark}  Q: {q}")
                print(f"         A: {answer[:120]}{'…' if len(answer) > 120 else ''}")

            query_elapsed = time.time() - t1
            print(f"\n    Query elapsed   : {query_elapsed:.1f} s")
            print(f"    Grounded        : {grounded_count} / {len(TEST_QUESTIONS)}")

            # ── 3. RAGAS Evaluation (optional) ─────────────────────────────────
            ragas_metrics = None
            if study_run_ragas:
                try:
                    from src.evaluation.ragas_runner import run_ragas_evaluation  # noqa: E402

                    print("\n[RAGAS] Running RAGAS evaluation...")
                    ragas_metrics = run_ragas_evaluation(run_ragas=True, max_samples=20)
                    print("\n    RAGAS metrics")
                    print(f"      faithfulness      : {ragas_metrics.get('faithfulness', 0.0):.4f}")
                    print(
                        f"      answer_relevancy  : {ragas_metrics.get('answer_relevancy', 0.0):.4f}"
                    )
                    print(
                        f"      context_precision : {ragas_metrics.get('context_precision', 0.0):.4f}"
                    )
                    print(
                        f"      context_recall    : {ragas_metrics.get('context_recall', 0.0):.4f}"
                    )
                except Exception as exc:  # noqa: BLE001
                    logger.warning("RAGAS evaluation failed: %s", exc)

            # ── Summary ────────────────────────────────────────────────────────
            total_elapsed = builder_elapsed + query_elapsed
            positive = (
                len(triplets) > 0
                and len(completed) == len(tables)
                and not failed
                and grounded_count == len(TEST_QUESTIONS)
            )

            print()
            print(sep())
            verdict = "✅  POSITIVE" if positive else "❌  NEGATIVE"
            print(f"  VERDICT  : {verdict}")
            print(f"  Total    : {total_elapsed:.1f} s")
            print(sep())

            result = {
                "study_id": study_id,
                "success": True,
                "builder_elapsed_s": round(builder_elapsed, 1),
                "query_elapsed_s": round(query_elapsed, 1),
                "total_elapsed_s": round(total_elapsed, 1),
                "triplets": len(triplets),
                "entities": len(entities),
                "tables_parsed": len(tables),
                "tables_enriched": len(enriched),
                "tables_completed": len(completed),
                "cypher_failed": bool(failed),
                "grounded_count": grounded_count,
                "question_count": len(TEST_QUESTIONS),
                "positive": bool(positive),
                "ragas": ragas_metrics,
                "env_overrides": env_overrides,
                "run_ragas": study_run_ragas,
                "timestamp": datetime.now(tz=UTC).isoformat(),
            }

            # Save JSON result
            json_file = RESULTS_DIR / f"{study_id}.json"
            with json_file.open("w", encoding="utf-8") as f:
                json.dump(result, f, indent=2)
            print(f"\n  Result saved to: {json_file}")
            print(f"  Log saved to:    {log_file}")

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
            "run_ragas": study_run_ragas,
            "timestamp": datetime.now(tz=UTC).isoformat(),
        }
    finally:
        # Restore original handlers
        root_logger.removeHandler(console_handler)
        root_logger.removeHandler(file_handler)
        file_handler.close()
        for handler in original_handlers:
            root_logger.addHandler(handler)

    return result


# ── Main orchestration ─────────────────────────────────────────────────────────


def run_all_studies(
    run_ragas: bool = False,
    single_study: str | None = None,
) -> dict[str, object]:
    """Run all or a subset of ablation studies.

    Args:
        run_ragas: If True, run RAGAS evaluation for studies that have it enabled.
        single_study: If provided, run only this study.

    Returns:
        A summary dict with all results.
    """
    print_header("Ablation Study Runner - Full Pipeline")

    # Determine which studies to run
    studies_to_run = [single_study] if single_study else sorted(ABLATION_MATRIX.keys())

    print(f"  Studies to run: {len(studies_to_run)}")
    print(f"  RAGAS enabled:  {run_ragas}")
    if studies_to_run:
        print(f"  {', '.join(studies_to_run)}")
    print()

    results: dict[str, dict[str, object]] = {}
    total_start = time.time()

    for i, study_id in enumerate(studies_to_run, 1):
        print(f"\n[{i}/{len(studies_to_run)}] Running {study_id}...")

        try:
            result = run_ablation_study(study_id, run_ragas=run_ragas)
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
        elapsed = r.get("total_elapsed_s", r.get("elapsed_s", "N/A"))
        pos = " POSITIVE" if r.get("positive", False) else " NEGATIVE"
        print(f"    {status} {study_id}: {elapsed}s |{pos}")

    # Save final summary
    summary_file = RESULTS_DIR / "ablation_summary.json"
    with summary_file.open("w", encoding="utf-8") as f:
        json.dump(
            {
                "timestamp": datetime.now(tz=UTC).isoformat(),
                "total_elapsed_s": round(total_elapsed, 1),
                "studies": results,
            },
            f,
            indent=2,
        )
    print(f"\n  Summary saved to: {summary_file}")

    return {
        "results": results,
        "total_elapsed_s": total_elapsed,
    }


# ── CLI ─────────────────────────────────────────────────────────────────────────


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Automated ablation study runner with full pipeline"
    )
    parser.add_argument(
        "--run-ragas",
        action="store_true",
        help="Run RAGAS evaluation for enabled studies",
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
        run_ragas=args.run_ragas,
        single_study=args.study,
    )


if __name__ == "__main__":
    main()
