"""AB-00 Diagnostic Script — 360-degree verbose logging.

Riusa il grafo Neo4j esistente (NON riesegue il builder).
Lancia le prime N domande del gold_standard con logging verbose per diagnosticare
i bassi RAGAS scores di AB-00.

Output (nella stessa cartella dello script):
  - retrieval_log.jsonl   : per ogni query, tutti i chunk recuperati per canale
  - answers_log.jsonl     : domanda, prompt inviato, risposta raw, risposta finale
  - grader_log.jsonl      : decisione grader, critique, prompt
  - report.md             : riepilogo leggibile a 360° con confronto gold_truth

Uso:
  cd /path/to/thesis
  source .venv/bin/activate
    python notebooks/ablation/diagnostics/diagnose_ab00.py [--questions N] [--no-grader]
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import textwrap
import time
from datetime import UTC, datetime
from pathlib import Path

# ── Repo root on path ──────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv  # type: ignore[import]

load_dotenv(ROOT / ".env")

os.environ.setdefault("NEO4J_URI", "bolt://localhost:7687")
os.environ.setdefault("NEO4J_USER", "neo4j")
os.environ.setdefault("NEO4J_PASSWORD", "test_password")
os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")

from src.config.llm_factory import reconfigure_from_env  # noqa: E402
from src.config.logging import setup_notebook_logging  # noqa: E402

reconfigure_from_env()
setup_notebook_logging()

# ── Paths ──────────────────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).parent
GOLD_STANDARD = ROOT / "tests" / "fixtures" / "00_legacy" / "gold_standard.json"

RETRIEVAL_LOG = SCRIPT_DIR / "retrieval_log.jsonl"
ANSWERS_LOG = SCRIPT_DIR / "answers_log.jsonl"
GRADER_LOG = SCRIPT_DIR / "grader_log.jsonl"
REPORT_MD = SCRIPT_DIR / "report.md"

# ── Logging setup ──────────────────────────────────────────────────────────────
log = logging.getLogger("diagnose_ab00")


# ─────────────────────────────────────────────────────────────────────────────
# Patched versions of retrieval / generation functions that capture internals
# ─────────────────────────────────────────────────────────────────────────────


def _run_query_verbose(
    question: str,
    gold: dict,
    retrieval_log_fh,
    answers_log_fh,
    grader_log_fh,
    run_grader: bool = True,
) -> dict:
    """Run the query graph with verbose interception at each stage.

    Returns a dict with all intermediate state captured.
    """
    from unittest.mock import patch

    from langchain_core.messages import HumanMessage, SystemMessage

    from src.config.llm_factory import get_reasoning_llm
    from src.config.settings import get_settings
    from src.generation.answer_generator import format_context, generate_answer
    from src.generation.hallucination_grader import grade_answer
    from src.graph.neo4j_client import Neo4jClient, setup_schema
    from src.models.schemas import GraderDecision
    from src.retrieval.embeddings import get_embeddings
    from src.retrieval.hybrid_retriever import (
        bm25_search,
        build_node_index,
        fetch_all_concepts,
        fetch_fk_relationships,
        graph_traversal,
        merge_results,
        vector_search,
    )
    from src.retrieval.reranker import rerank

    settings = get_settings()
    llm = get_reasoning_llm()
    embeddings_model = get_embeddings()
    record: dict = {"question": question, "timestamp": datetime.now(tz=UTC).isoformat()}

    # ── 1. Retrieval ────────────────────────────────────────────────────────────
    log.info("  [Retrieval] starting for: %s", question[:70])
    with Neo4jClient() as client:
        setup_schema(client)
        t0 = time.time()

        all_nodes = build_node_index(client)
        record["graph_node_count"] = len(all_nodes)

        vec_results = vector_search(
            question, client, top_k=settings.retrieval_vector_top_k, model=embeddings_model
        )
        graph_trav = graph_traversal(
            seed_names=[c.node_id for c in vec_results[:5]],
            client=client,
            depth=settings.retrieval_graph_depth,
        )
        all_concepts = fetch_all_concepts(client)
        fk_chunks = fetch_fk_relationships(client)
        bm25_results = bm25_search(question, all_nodes, top_k=settings.retrieval_bm25_top_k)
        merged = merge_results(vec_results, bm25_results, graph_trav + all_concepts + fk_chunks)

        retrieval_elapsed = time.time() - t0
        record["retrieval_elapsed_s"] = round(retrieval_elapsed, 2)

    # -- Capture retrieval detail
    def _chunk_to_dict(c, channel: str) -> dict:
        return {
            "node_id": c.node_id,
            "node_type": c.node_type,
            "source_type": c.source_type,
            "score": round(c.score, 4),
            "text_preview": c.text[:200],
            "channel": channel,
        }

    record["retrieval"] = {
        "vector": [_chunk_to_dict(c, "vector") for c in vec_results],
        "bm25": [_chunk_to_dict(c, "bm25") for c in bm25_results],
        "graph_traversal": [_chunk_to_dict(c, "graph") for c in graph_trav],
        "all_concepts": [_chunk_to_dict(c, "concepts") for c in all_concepts],
        "fk_chunks": [_chunk_to_dict(c, "fk") for c in fk_chunks],
        "merged_top20": [_chunk_to_dict(c, c.source_type) for c in merged[:20]],
        "total_merged": len(merged),
    }

    log.info(
        "  [Retrieval] vector=%d  bm25=%d  graph=%d  concepts=%d  fk=%d  merged=%d",
        len(vec_results),
        len(bm25_results),
        len(graph_trav),
        len(all_concepts),
        len(fk_chunks),
        len(merged),
    )

    retrieval_log_fh.write(json.dumps(record["retrieval"] | {"question": question}) + "\n")
    retrieval_log_fh.flush()

    # ── 2. Reranking ────────────────────────────────────────────────────────────
    log.info("  [Reranker] reranking %d chunks → top %d", len(merged), settings.reranker_top_k)
    t1 = time.time()
    reranked = rerank(question, merged, top_k=settings.reranker_top_k)
    record["reranking_elapsed_s"] = round(time.time() - t1, 2)
    record["reranked"] = [_chunk_to_dict(c, c.source_type) for c in reranked]

    log.info("  [Reranker] top %d chunks after reranking:", len(reranked))
    for i, c in enumerate(reranked, 1):
        log.info("    [%2d] score=%.4f  %-20s  %s", i, c.score, c.node_id, c.text[:80])

    # ── 3. Context block sent to LLM ───────────────────────────────────────────
    context_block = format_context(reranked)
    record["context_block"] = context_block

    # Check against gold standard context
    gold_contexts = gold.get("ground_truth_contexts", [])
    reranked_texts = [c.text for c in reranked]
    gold_hit = sum(
        1 for gc in gold_contexts if any(gc[:40].lower() in rt.lower() for rt in reranked_texts)
    )
    record["gold_context_hit"] = f"{gold_hit}/{len(gold_contexts)}"
    log.info("  [Context] gold context coverage: %s", record["gold_context_hit"])

    # ── 4. Answer generation ───────────────────────────────────────────────────
    log.info("  [Answer] generating answer…")
    t2 = time.time()
    answer = generate_answer(question, reranked, llm)
    record["answer_elapsed_s"] = round(time.time() - t2, 2)
    record["answer"] = answer
    record["ground_truth"] = gold.get("ground_truth", "")

    log.info("  [Answer] (%ds) %s", int(record["answer_elapsed_s"]), answer[:150])

    answers_log_fh.write(
        json.dumps(
            {
                "question": question,
                "context_block": context_block,
                "answer": answer,
                "ground_truth": gold.get("ground_truth", ""),
                "reranked_chunks": record["reranked"],
                "gold_context_hit": record["gold_context_hit"],
                "answer_elapsed_s": record["answer_elapsed_s"],
            }
        )
        + "\n"
    )
    answers_log_fh.flush()

    # ── 5. Hallucination grader ────────────────────────────────────────────────
    grader_decision = None
    if run_grader and settings.enable_hallucination_grader:
        log.info("  [Grader] evaluating answer faithfulness…")
        t3 = time.time()
        grader_decision = grade_answer(question, answer, reranked, llm)
        record["grader_elapsed_s"] = round(time.time() - t3, 2)
        record["grader"] = {
            "grounded": grader_decision.grounded,
            "action": grader_decision.action,
            "critique": grader_decision.critique,
        }
        log.info(
            "  [Grader] grounded=%s  action=%s  critique=%s",
            grader_decision.grounded,
            grader_decision.action,
            (grader_decision.critique or "(none)")[:120],
        )
        grader_log_fh.write(
            json.dumps(
                {
                    "question": question,
                    "answer": answer,
                    "grounded": grader_decision.grounded,
                    "action": grader_decision.action,
                    "critique": grader_decision.critique,
                    "grader_elapsed_s": record["grader_elapsed_s"],
                    "num_chunks_passed": len(reranked),
                }
            )
            + "\n"
        )
        grader_log_fh.flush()

    return record


# ─────────────────────────────────────────────────────────────────────────────
# Report generation
# ─────────────────────────────────────────────────────────────────────────────


def _write_report(all_records: list[dict]) -> None:
    """Write a human-readable Markdown report with the diagnostic results."""
    lines: list[str] = [
        "# AB-00 Diagnostic Report",
        f"\nGenerated: {datetime.now(tz=UTC).isoformat()}",
        f"\nQuestions evaluated: **{len(all_records)}**",
        "\n---\n",
    ]

    # ── Summary table ──────────────────────────────────────────────────────────
    lines += [
        "## Summary Table\n",
        "| # | Question (short) | Graph nodes | Vec | BM25 | Graph | Merged | Reranked | Gold ctx hit | Grounded | Answer (preview) |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for i, r in enumerate(all_records, 1):
        q_short = r["question"][:45].replace("|", "/")
        ret = r.get("retrieval", {})
        grader = r.get("grader", {})
        grounded_str = (
            "✅" if grader.get("grounded", True) else f"❌ {(grader.get('critique') or '')[:30]}"
        )
        ans_preview = r.get("answer", "")[:60].replace("|", "/").replace("\n", " ")
        lines.append(
            f"| {i} | {q_short} "
            f"| {r.get('graph_node_count', '?')} "
            f"| {len(ret.get('vector', []))} "
            f"| {len(ret.get('bm25', []))} "
            f"| {len(ret.get('graph_traversal', []))} "
            f"| {ret.get('total_merged', '?')} "
            f"| {len(r.get('reranked', []))} "
            f"| {r.get('gold_context_hit', '?')} "
            f"| {grounded_str} "
            f"| {ans_preview} |"
        )

    # ── Per-question detail ────────────────────────────────────────────────────
    lines += ["\n---\n", "## Per-Question Detail\n"]
    for i, r in enumerate(all_records, 1):
        q = r["question"]
        grader = r.get("grader", {})
        lines += [
            f"### Q{i}: {q}",
            "",
            f"**Gold truth:** {r.get('ground_truth', '')[:200]}",
            "",
            f"**Answer generated:** {r.get('answer', '')[:300]}",
            "",
        ]

        # Grader decision
        if grader:
            grounded_icon = "✅" if grader.get("grounded") else "❌"
            lines.append(
                f"**Grader:** {grounded_icon} grounded={grader.get('grounded')}  "
                f"action=`{grader.get('action')}`"
            )
            if grader.get("critique"):
                lines.append(f"> **Critique:** {grader['critique']}")
            lines.append("")

        # Top reranked chunks
        lines.append("**Top reranked chunks (sent to LLM as context):**")
        lines.append("")
        lines.append("| Rank | node_id | type | score | source | text preview |")
        lines.append("|---:|---|---|---:|---|---|")
        for j, ch in enumerate(r.get("reranked", [])[:10], 1):
            text_prev = ch.get("text_preview", "")[:80].replace("|", "/").replace("\n", " ")
            lines.append(
                f"| {j} | {ch.get('node_id', '')} | {ch.get('node_type', '')} "
                f"| {ch.get('score', 0):.4f} | {ch.get('source_type', '')} | {text_prev} |"
            )

        # Gold context compared to retrieved
        lines += [
            "",
            f"**Gold context hit:** `{r.get('gold_context_hit', '?')}`  "
            f"(retrieval={r.get('retrieval_elapsed_s', '?')}s  "
            f"rerank={r.get('reranking_elapsed_s', '?')}s  "
            f"answer={r.get('answer_elapsed_s', '?')}s)",
            "",
            "---",
            "",
        ]

    # ── Aggregate stats ────────────────────────────────────────────────────────
    lines += ["## Aggregate Statistics\n"]
    grounded_total = sum(1 for r in all_records if r.get("grader", {}).get("grounded", True))
    lines.append(f"- **Grounded answers:** {grounded_total}/{len(all_records)}")

    avg_vec = sum(len(r.get("retrieval", {}).get("vector", [])) for r in all_records) / max(
        len(all_records), 1
    )
    avg_merged = sum(r.get("retrieval", {}).get("total_merged", 0) for r in all_records) / max(
        len(all_records), 1
    )
    avg_reranked = sum(len(r.get("reranked", [])) for r in all_records) / max(len(all_records), 1)
    lines += [
        f"- **Avg vector results:** {avg_vec:.1f}",
        f"- **Avg merged pool:** {avg_merged:.1f}",
        f"- **Avg reranked chunks:** {avg_reranked:.1f}",
    ]

    # Gold context coverage
    def _parse_hit(s: str) -> tuple[int, int]:
        try:
            a, b = s.split("/")
            return int(a), int(b)
        except Exception:
            return 0, 0

    hits = [_parse_hit(r.get("gold_context_hit", "0/0")) for r in all_records]
    total_hit = sum(h for h, _ in hits)
    total_gold = sum(t for _, t in hits)
    coverage = total_hit / total_gold if total_gold > 0 else 0.0
    lines.append(f"- **Gold context coverage:** {total_hit}/{total_gold} = {coverage:.1%}")

    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    log.info("Report written to %s", REPORT_MD)


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────


def main() -> None:
    parser = argparse.ArgumentParser(description="AB-00 360-degree diagnostic")
    parser.add_argument(
        "--questions",
        type=int,
        default=20,
        help="Number of gold_standard questions to evaluate (default: 20)",
    )
    parser.add_argument(
        "--no-grader",
        action="store_true",
        help="Skip hallucination grader (faster run)",
    )
    args = parser.parse_args()

    # Load gold standard
    with GOLD_STANDARD.open(encoding="utf-8") as f:
        gold_data: list[dict] = json.load(f)
    gold_data = gold_data[: args.questions]

    log.info("=" * 60)
    log.info("AB-00 Diagnostic — %d questions", len(gold_data))
    log.info("Output dir: %s", SCRIPT_DIR)
    log.info("=" * 60)

    all_records: list[dict] = []

    with (
        RETRIEVAL_LOG.open("w", encoding="utf-8") as ret_fh,
        ANSWERS_LOG.open("w", encoding="utf-8") as ans_fh,
        GRADER_LOG.open("w", encoding="utf-8") as grd_fh,
    ):
        for i, gold in enumerate(gold_data, 1):
            q = gold["question"]
            log.info("")
            log.info("── Q%d/%d: %s", i, len(gold_data), q)
            t_start = time.time()
            try:
                rec = _run_query_verbose(
                    question=q,
                    gold=gold,
                    retrieval_log_fh=ret_fh,
                    answers_log_fh=ans_fh,
                    grader_log_fh=grd_fh,
                    run_grader=not args.no_grader,
                )
                rec["index"] = i
                all_records.append(rec)
                log.info("  ✓ done in %.1fs", time.time() - t_start)
            except Exception:
                log.exception("  ✗ Q%d failed — skipping", i)

    # Write the Markdown report
    _write_report(all_records)

    # Print quick summary to console
    print("\n" + "=" * 60)
    print(f"DONE — {len(all_records)} questions evaluated")
    grounded = sum(1 for r in all_records if r.get("grader", {}).get("grounded", True))
    print(f"Grounded: {grounded}/{len(all_records)}")
    hits = []
    for r in all_records:
        try:
            a, b = r.get("gold_context_hit", "0/0").split("/")
            hits.append((int(a), int(b)))
        except Exception:
            pass
    if hits:
        total_h = sum(h for h, _ in hits)
        total_t = sum(t for _, t in hits)
        print(f"Gold ctx coverage: {total_h}/{total_t} = {total_h / total_t:.1%}")
    print(f"\nFiles written:")
    for p in [RETRIEVAL_LOG, ANSWERS_LOG, GRADER_LOG, REPORT_MD]:
        print(f"  {p}")
    print("=" * 60)


if __name__ == "__main__":
    main()
