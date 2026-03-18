"""Headless pipeline runner — replicates the notebook end-to-end.

Usage:
    python scripts/pipeline_run.py [--run-id N]

Runs:
1. Builder Graph  (triplet extraction → ER → mapping → Cypher upsert)
2. Query Graph    (4 standard test questions)

Prints a compact summary and exits with code 0 on success, 1 on failure.
A run is considered "positive" when:
  - triplets_extracted  > 0
  - tables_completed   == 3
  - cypher_failed      == False
  - all 4 Q&A answers graded as grounded (action=pass)
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import time
from pathlib import Path

# ── Repo root on path ──────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

# ── Load .env ─────────────────────────────────────────────────────────────────
from dotenv import load_dotenv  # type: ignore[import]

load_dotenv(ROOT / ".env")

# ── Pipeline config (matches notebook defaults) ────────────────────────────────
os.environ.setdefault("NEO4J_URI", "bolt://localhost:7687")
os.environ.setdefault("NEO4J_USER", "neo4j")
os.environ.setdefault("NEO4J_PASSWORD", "test_password")
os.environ.setdefault("LLM_MODEL_REASONING", "openai/gpt-oss-120b")
os.environ.setdefault("LLM_MODEL_EXTRACTION", "openai/gpt-oss-20b")
os.environ.setdefault("LLM_MAX_TOKENS_REASONING", "16384")
os.environ.setdefault("LLM_MAX_TOKENS_EXTRACTION", "8192")
os.environ.setdefault("EXTRACTION_CONCURRENCY", "5")
os.environ.setdefault("ER_SIMILARITY_THRESHOLD", "0.75")
os.environ.setdefault("RETRIEVAL_VECTOR_TOP_K", "20")
os.environ.setdefault("RETRIEVAL_BM25_TOP_K", "10")
os.environ.setdefault("RERANKER_TOP_K", "10")
# Avoid network retries from HF Hub in offline/no-internet environments.
os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")

# ── Notebook-style logging ─────────────────────────────────────────────────────
from src.config.llm_factory import reconfigure_from_env  # noqa: E402
from src.config.logging import setup_notebook_logging  # noqa: E402

reconfigure_from_env()
setup_notebook_logging()

logger = logging.getLogger("pipeline_run")

# ── Data fixtures ─────────────────────────────────────────────────────────────
FIXTURE_DIR = ROOT / "tests" / "fixtures"
DOC_PATHS = [
    FIXTURE_DIR / "sample_docs" / "business_glossary.txt",
    FIXTURE_DIR / "sample_docs" / "data_dictionary.txt",
]
DDL_PATHS = [FIXTURE_DIR / "sample_ddl" / "simple_schema.sql"]

# ── Test questions (same as notebook batch cell) ──────────────────────────────
TEST_QUESTIONS = [
    "What entities exist in the business domain?",
    "Which table stores customer information?",
    "How are customers and orders related?",
    "What columns does the product table have?",
]


def sep(char: str = "─", n: int = 60) -> str:
    return char * n


def run_pipeline(run_id: int = 1, run_ragas: bool = False) -> dict[str, object]:
    """Execute one full pipeline run and return a structured summary."""
    print()
    print(sep("═"))
    print(f"  RUN {run_id:02d}  —  {time.strftime('%Y-%m-%dT%H:%M:%S')}")
    print(sep("═"))

    # ── 1. Builder Graph ───────────────────────────────────────────────────────
    from src.graph.builder_graph import run_builder

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
    if completed:
        for t in completed:
            print(f"      ✓ {t}")

    # ── 2. Query Graph ─────────────────────────────────────────────────────────
    from src.generation.query_graph import run_query

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

    # ── Summary ────────────────────────────────────────────────────────────────
    total_elapsed = builder_elapsed + query_elapsed
    positive = (
        len(triplets) > 0
        and len(completed) == len(tables)
        and not failed
        and grounded_count == len(TEST_QUESTIONS)
    )

    print()
    ragas_metrics: dict[str, float] | None = None
    if run_ragas:
        try:
            from src.evaluation.ragas_runner import run_ragas_evaluation

            ragas_metrics = run_ragas_evaluation(evaluator_model="openai/gpt-oss-20b")
            print("\n    RAGAS metrics")
            print(f"      faithfulness      : {ragas_metrics.get('faithfulness', 0.0):.4f}")
            print(f"      answer_relevancy  : {ragas_metrics.get('answer_relevancy', 0.0):.4f}")
            print(f"      context_precision : {ragas_metrics.get('context_precision', 0.0):.4f}")
            print(f"      context_recall    : {ragas_metrics.get('context_recall', 0.0):.4f}")
        except Exception as exc:  # noqa: BLE001
            logger.warning("RAGAS evaluation failed: %s", exc)

    print(sep())
    verdict = "✅  POSITIVE" if positive else "❌  NEGATIVE"
    print(f"  VERDICT  : {verdict}")
    print(f"  Total    : {total_elapsed:.1f} s")
    print(sep())

    return {
        "run_id": run_id,
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
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Headless pipeline test runner")
    parser.add_argument("--run-id", type=int, default=1, help="Run identifier label")
    parser.add_argument(
        "--set",
        action="append",
        default=[],
        metavar="KEY=VALUE",
        help="Override environment variable(s) for this run",
    )
    parser.add_argument(
        "--run-ragas",
        action="store_true",
        help="Run RAGAS evaluation after the pipeline run",
    )
    parser.add_argument(
        "--json-out",
        type=str,
        default="",
        help="Optional output path for run summary JSON",
    )
    args = parser.parse_args()
    for kv in args.set:
        if "=" not in kv:
            raise ValueError(f"Invalid --set value '{kv}'. Expected KEY=VALUE.")
        k, v = kv.split("=", 1)
        os.environ[k] = v
    if args.set:
        reconfigure_from_env()

    summary = run_pipeline(run_id=args.run_id, run_ragas=args.run_ragas)
    if args.json_out:
        out = Path(args.json_out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    sys.exit(0 if bool(summary["positive"]) else 1)


if __name__ == "__main__":
    main()
