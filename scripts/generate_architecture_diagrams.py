"""Generate architecture diagrams for the Builder and Query graphs.

Outputs:
  - docs/images/builder_graph.png
  - docs/images/query_graph.png
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

OUTPUT_DIR = Path(__file__).parent.parent / "docs" / "images"


def _draw_builder_graph() -> None:
    """Draw the Builder Graph architecture diagram."""
    fig, ax = plt.subplots(1, 1, figsize=(10, 14))
    ax.set_xlim(-5, 5)
    ax.set_ylim(-15.5, 1.5)
    ax.axis("off")
    ax.set_aspect("equal")

    # Colors
    c_input = "#E3F2FD"    # light blue
    c_extract = "#FFF3E0"  # light orange
    c_resolve = "#E8F5E9"  # light green
    c_map = "#F3E5F5"      # light purple
    c_build = "#FBE9E7"    # light red
    c_db = "#263238"       # dark
    c_loop = "#FF6F00"     # amber (loop arrows)
    c_edge = "#546E7A"     # blue-grey

    box_w, box_h = 3.2, 0.8

    def _box(cx, cy, label, color, fontsize=9, bold=False):
        rect = mpatches.FancyBboxPatch(
            (cx - box_w / 2, cy - box_h / 2), box_w, box_h,
            boxstyle="round,pad=0.1", facecolor=color, edgecolor="#37474F", linewidth=1.2
        )
        ax.add_patch(rect)
        weight = "bold" if bold else "normal"
        ax.text(cx, cy, label, ha="center", va="center", fontsize=fontsize, weight=weight)

    def _arrow(x1, y1, x2, y2, color=c_edge, style="-"):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color=color, lw=1.5, linestyle=style))

    def _loop_arrow(x, y1, y2, side="right", label=""):
        """Draw a loop arrow on the side."""
        offset = 2.2 if side == "right" else -2.2
        mid_y = (y1 + y2) / 2
        ax.annotate("", xy=(x + offset * 0.3, y2 + box_h / 2), xytext=(x + offset * 0.3, y1 - box_h / 2),
                    arrowprops=dict(arrowstyle="->", color=c_loop, lw=1.8,
                                    connectionstyle=f"arc3,rad={-0.4 if side == 'right' else 0.4}"))
        if label:
            ax.text(x + offset * 0.85, mid_y, label, ha="center", va="center",
                    fontsize=7, color=c_loop, style="italic")

    # ── Input nodes ──
    y = 1.0
    ax.text(-2, y, "Business Docs\n(PDF/TXT)", ha="center", va="center", fontsize=9,
            bbox=dict(boxstyle="round", facecolor=c_input, edgecolor="#90CAF9"))
    ax.text(2, y, "DDL Schemas\n(SQL)", ha="center", va="center", fontsize=9,
            bbox=dict(boxstyle="round", facecolor=c_input, edgecolor="#90CAF9"))

    # ── Extract / Parse ──
    y_extract = -0.5
    _box(-2, y_extract, "Triplet Extraction\n(SLM: gpt-5-nano)", c_extract, fontsize=8)
    _box(2, y_extract, "DDL Parse + Schema\nEnrichment (LLM)", c_extract, fontsize=8)
    _arrow(-2, 1.0 - 0.3, -2, y_extract + box_h / 2)
    _arrow(2, 1.0 - 0.3, 2, y_extract + box_h / 2)

    # ── Entity Resolution ──
    y_er = -2.0
    _box(-2, y_er, "Entity Resolution\n(K-NN + LLM Judge)", c_resolve, fontsize=8)
    _arrow(-2, y_extract - box_h / 2, -2, y_er + box_h / 2)

    # ── RAG Mapping ──
    y_map = -4.0
    _box(0, y_map, "RAG Mapping\n(Map-Reduce per table)", c_map, fontsize=8, bold=True)
    _arrow(-2, y_er - box_h / 2, 0, y_map + box_h / 2)
    _arrow(2, y_extract - box_h / 2, 0, y_map + box_h / 2)

    # ── Validate (Actor-Critic) ──
    y_val = -5.5
    _box(0, y_val, "Actor-Critic\nValidation", c_map, fontsize=8, bold=True)
    _arrow(0, y_map - box_h / 2, 0, y_val + box_h / 2)

    # Loop arrow: validate → rag_mapping
    ax.annotate("", xy=(box_w / 2 + 0.15, y_map), xytext=(box_w / 2 + 0.15, y_val),
                arrowprops=dict(arrowstyle="->", color=c_loop, lw=1.8,
                                connectionstyle="arc3,rad=-0.5"))
    ax.text(box_w / 2 + 1.1, (y_map + y_val) / 2, "Reflection\nLoop (≤3×)",
            ha="center", va="center", fontsize=7, color=c_loop, style="italic")

    # ── HITL ──
    y_hitl = -7.0
    _box(-2.5, y_hitl, "HITL\n(low confidence)", "#FFFDE7", fontsize=8)
    ax.annotate("", xy=(-2.5 + box_w / 2, y_hitl), xytext=(0 - box_w / 2, y_val),
                arrowprops=dict(arrowstyle="->", color="#FBC02D", lw=1.2, linestyle="--"))
    ax.text(-2.8, (y_val + y_hitl) / 2 + 0.2, "if conf < gate", ha="center", va="center",
            fontsize=6.5, color="#F57F17", style="italic")

    # ── Generate Cypher ──
    y_cypher = -7.0
    _box(0, y_cypher, "Cypher Generation\n(LLM)", c_build, fontsize=8)
    _arrow(0, y_val - box_h / 2, 0, y_cypher + box_h / 2)

    # ── Heal Cypher ──
    y_heal = -8.5
    _box(0, y_heal, "Cypher Healing\n(EXPLAIN + LLM)", c_build, fontsize=8)
    _arrow(0, y_cypher - box_h / 2, 0, y_heal + box_h / 2)

    # Loop arrow: heal → cypher
    ax.annotate("", xy=(-box_w / 2 - 0.15, y_cypher), xytext=(-box_w / 2 - 0.15, y_heal),
                arrowprops=dict(arrowstyle="->", color=c_loop, lw=1.8,
                                connectionstyle="arc3,rad=0.5"))
    ax.text(-box_w / 2 - 1.3, (y_cypher + y_heal) / 2, "Healing\nLoop (≤3×)",
            ha="center", va="center", fontsize=7, color=c_loop, style="italic")

    # ── Build Graph ──
    y_build = -10.0
    _box(0, y_build, "Neo4j Upsert\n(MERGE + FK edges)", c_build, fontsize=8)
    _arrow(0, y_heal - box_h / 2, 0, y_build + box_h / 2)

    # Loop arrow: build → rag_mapping (next table)
    ax.annotate("", xy=(box_w / 2 + 0.8, y_map), xytext=(box_w / 2 + 0.8, y_build),
                arrowprops=dict(arrowstyle="->", color=c_loop, lw=1.5, linestyle=":",
                                connectionstyle="arc3,rad=-0.3"))
    ax.text(box_w / 2 + 2.2, (y_map + y_build) / 2, "Next Table\n(FIFO queue)",
            ha="center", va="center", fontsize=7, color=c_loop, style="italic")

    # ── Neo4j KG ──
    y_kg = -11.8
    rect = mpatches.FancyBboxPatch(
        (-box_w / 2 - 0.3, y_kg - 0.5), box_w + 0.6, 1.0,
        boxstyle="round,pad=0.15", facecolor=c_db, edgecolor="#455A64", linewidth=2
    )
    ax.add_patch(rect)
    ax.text(0, y_kg, "Neo4j Knowledge Graph", ha="center", va="center",
            fontsize=10, weight="bold", color="white")
    _arrow(0, y_build - box_h / 2, 0, y_kg + 0.5)

    # ── Title ──
    ax.set_title("Builder Graph — LangGraph Architecture", fontsize=13, weight="bold", pad=15)

    # ── Legend ──
    legend_elements = [
        mpatches.Patch(facecolor=c_extract, edgecolor="#37474F", label="Extraction & Parsing"),
        mpatches.Patch(facecolor=c_resolve, edgecolor="#37474F", label="Entity Resolution"),
        mpatches.Patch(facecolor=c_map, edgecolor="#37474F", label="Mapping & Validation"),
        mpatches.Patch(facecolor=c_build, edgecolor="#37474F", label="Cypher & Upsert"),
        mpatches.Patch(facecolor=c_loop, edgecolor=c_loop, label="Self-Reflection Loop"),
    ]
    ax.legend(handles=legend_elements, loc="lower right", fontsize=8, framealpha=0.9)

    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "builder_graph.png", dpi=150, bbox_inches="tight",
                facecolor="white", edgecolor="none")
    plt.close(fig)
    print(f"  ✓ {OUTPUT_DIR / 'builder_graph.png'}")


def _draw_query_graph() -> None:
    """Draw the Query Graph architecture diagram."""
    fig, ax = plt.subplots(1, 1, figsize=(9, 12))
    ax.set_xlim(-5, 5)
    ax.set_ylim(-13.5, 1.5)
    ax.axis("off")
    ax.set_aspect("equal")

    # Colors
    c_input = "#E3F2FD"
    c_retrieval = "#E8F5E9"
    c_gen = "#FFF3E0"
    c_grade = "#FCE4EC"
    c_output = "#263238"
    c_loop = "#FF6F00"
    c_edge = "#546E7A"
    c_gate = "#FBC02D"

    box_w, box_h = 3.5, 0.8

    def _box(cx, cy, label, color, fontsize=9, bold=False):
        rect = mpatches.FancyBboxPatch(
            (cx - box_w / 2, cy - box_h / 2), box_w, box_h,
            boxstyle="round,pad=0.1", facecolor=color, edgecolor="#37474F", linewidth=1.2
        )
        ax.add_patch(rect)
        weight = "bold" if bold else "normal"
        ax.text(cx, cy, label, ha="center", va="center", fontsize=fontsize, weight=weight)

    def _arrow(x1, y1, x2, y2, color=c_edge, style="-"):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color=color, lw=1.5, linestyle=style))

    # ── Input ──
    y = 1.0
    ax.text(0, y, "Natural Language Question", ha="center", va="center", fontsize=10,
            bbox=dict(boxstyle="round", facecolor=c_input, edgecolor="#90CAF9", linewidth=1.5))

    # ── Hybrid Retrieval ──
    y_ret = -0.5
    _box(0, y_ret, "Hybrid Retrieval\n(Dense + BM25 + Graph Traversal)", c_retrieval, fontsize=8)
    _arrow(0, y - 0.3, 0, y_ret + box_h / 2)

    # ── Reranking ──
    y_rerank = -2.0
    _box(0, y_rerank, "Cross-Encoder Reranking\n(bge-reranker-v2-m3)", c_retrieval, fontsize=8)
    _arrow(0, y_ret - box_h / 2, 0, y_rerank + box_h / 2)

    # ── Quality Gate ──
    y_gate = -3.5
    # Diamond shape for decision
    diamond_size = 0.6
    diamond = plt.Polygon(
        [[0, y_gate + diamond_size], [diamond_size * 1.5, y_gate],
         [0, y_gate - diamond_size], [-diamond_size * 1.5, y_gate]],
        closed=True, facecolor="#FFF9C4", edgecolor="#F57F17", linewidth=1.5
    )
    ax.add_patch(diamond)
    ax.text(0, y_gate, "Quality\nGate", ha="center", va="center", fontsize=7, weight="bold")
    _arrow(0, y_rerank - box_h / 2, 0, y_gate + diamond_size)

    # Abstain branch
    ax.annotate("", xy=(-3, y_gate), xytext=(-diamond_size * 1.5, y_gate),
                arrowprops=dict(arrowstyle="->", color=c_gate, lw=1.5, linestyle="--"))
    ax.text(-3.5, y_gate + 0.3, "abstain", ha="center", va="center",
            fontsize=7, color="#F57F17", style="italic")
    ax.text(-3.5, y_gate - 0.3, '"Cannot find\nsufficient context"', ha="center", va="center",
            fontsize=6.5, color="#795548")

    # ── Context Distillation ──
    y_ctx = -5.0
    _box(0, y_ctx, "Context Distillation\n(adequate / sparse / insufficient)", c_gen, fontsize=8)
    _arrow(0, y_gate - diamond_size, 0, y_ctx + box_h / 2)

    # ── Answer Generation ──
    y_ans = -6.8
    _box(0, y_ans, "Answer Generation\n(Context-adaptive LLM)", c_gen, fontsize=8, bold=True)
    _arrow(0, y_ctx - box_h / 2, 0, y_ans + box_h / 2)

    # ── Hallucination Grader ──
    y_grade = -8.5
    _box(0, y_grade, "Hallucination Grader\n(Self-RAG structured critique)", c_grade, fontsize=8, bold=True)
    _arrow(0, y_ans - box_h / 2, 0, y_grade + box_h / 2)

    # ── Consistency Validator ──
    y_cons = -10.0
    _box(0, y_cons, "Grader Consistency\nValidator", c_grade, fontsize=8)
    _arrow(0, y_grade - box_h / 2, 0, y_cons + box_h / 2)

    # Loop arrow: consistency → answer_gen (regenerate)
    ax.annotate("", xy=(box_w / 2 + 0.15, y_ans), xytext=(box_w / 2 + 0.15, y_cons),
                arrowprops=dict(arrowstyle="->", color=c_loop, lw=1.8,
                                connectionstyle="arc3,rad=-0.5"))
    ax.text(box_w / 2 + 1.4, (y_ans + y_cons) / 2, "Regenerate\nLoop (≤3×)",
            ha="center", va="center", fontsize=7, color=c_loop, style="italic")

    # ── Output ──
    y_out = -11.8
    rect = mpatches.FancyBboxPatch(
        (-box_w / 2, y_out - 0.4), box_w, 0.8,
        boxstyle="round,pad=0.1", facecolor=c_output, edgecolor="#455A64", linewidth=2
    )
    ax.add_patch(rect)
    ax.text(0, y_out, "Grounded Answer + Sources", ha="center", va="center",
            fontsize=10, weight="bold", color="white")
    _arrow(0, y_cons - box_h / 2, 0, y_out + 0.4)

    # ── Title ──
    ax.set_title("Query Graph — LangGraph Architecture", fontsize=13, weight="bold", pad=15)

    # ── Legend ──
    legend_elements = [
        mpatches.Patch(facecolor=c_retrieval, edgecolor="#37474F", label="Retrieval & Reranking"),
        mpatches.Patch(facecolor=c_gen, edgecolor="#37474F", label="Context & Generation"),
        mpatches.Patch(facecolor=c_grade, edgecolor="#37474F", label="Hallucination Grading"),
        mpatches.Patch(facecolor=c_loop, edgecolor=c_loop, label="Self-RAG Loop"),
        mpatches.Patch(facecolor="#FFF9C4", edgecolor="#F57F17", label="Decision Gate"),
    ]
    ax.legend(handles=legend_elements, loc="lower right", fontsize=8, framealpha=0.9)

    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "query_graph.png", dpi=150, bbox_inches="tight",
                facecolor="white", edgecolor="none")
    plt.close(fig)
    print(f"  ✓ {OUTPUT_DIR / 'query_graph.png'}")


def _draw_system_overview() -> None:
    """Draw the high-level System Overview diagram (CQRS two-graph architecture)."""
    fig, ax = plt.subplots(1, 1, figsize=(14, 8))
    ax.set_xlim(-7.5, 7.5)
    ax.set_ylim(-5.5, 3.5)
    ax.axis("off")
    ax.set_aspect("equal")

    # Colors — consistent with builder/query graph palettes
    c_input = "#E3F2FD"     # light blue
    c_builder = "#FFF3E0"   # light orange (extraction tones)
    c_builder_box = "#FFE0B2"
    c_kg = "#263238"        # dark (Neo4j)
    c_query = "#E8F5E9"     # light green (retrieval tones)
    c_query_box = "#C8E6C9"
    c_output = "#263238"    # dark
    c_edge = "#546E7A"
    c_loop = "#FF6F00"
    c_phase = "#78909C"

    # ── Helper functions (same style as builder/query) ──
    def _box(cx, cy, w, h, label, color, fontsize=9, bold=False, edgecolor="#37474F"):
        rect = mpatches.FancyBboxPatch(
            (cx - w / 2, cy - h / 2), w, h,
            boxstyle="round,pad=0.12", facecolor=color, edgecolor=edgecolor, linewidth=1.2
        )
        ax.add_patch(rect)
        weight = "bold" if bold else "normal"
        ax.text(cx, cy, label, ha="center", va="center", fontsize=fontsize,
                weight=weight, linespacing=1.4)

    def _arrow(x1, y1, x2, y2, color=c_edge, lw=1.5, style="-"):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color=color, lw=lw, linestyle=style))

    def _darrow(x1, y1, x2, y2, color=c_edge, lw=1.5):
        """Double-headed arrow."""
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="<->", color=color, lw=lw))

    # ══════════════════════════════════════════════════════
    # LEFT SIDE — Inputs
    # ══════════════════════════════════════════════════════
    _box(-6, 2.0, 2.6, 0.7, "PDF / TXT\nBusiness Documents", c_input, fontsize=8)
    _box(-6, 0.8, 2.6, 0.7, "DDL / SQL\nDatabase Schemas", c_input, fontsize=8)

    # ══════════════════════════════════════════════════════
    # CENTER-LEFT — Builder Graph (simplified)
    # ══════════════════════════════════════════════════════
    # Outer rounded rectangle for Builder
    builder_rect = mpatches.FancyBboxPatch(
        (-4.2, -2.8), 4.0, 5.5,
        boxstyle="round,pad=0.2", facecolor=c_builder, edgecolor="#E65100",
        linewidth=2, alpha=0.35
    )
    ax.add_patch(builder_rect)
    ax.text(-2.2, 2.3, "Builder Graph", ha="center", va="center",
            fontsize=11, weight="bold", color="#BF360C")
    ax.text(-2.2, 1.8, "(Write path — batch)", ha="center", va="center",
            fontsize=7, color="#BF360C", style="italic")

    # Builder internal nodes
    _box(-2.2, 1.0, 3.2, 0.55, "Ingestion & Chunking", c_builder_box, fontsize=7.5)
    _box(-2.2, 0.1, 3.2, 0.55, "Triplet Extraction + ER", c_builder_box, fontsize=7.5)
    _box(-2.2, -0.8, 3.2, 0.55, "Schema Parsing & Enrichment", c_builder_box, fontsize=7.5)
    _box(-2.2, -1.7, 3.2, 0.55, "Semantic Mapping (Actor-Critic)", c_builder_box, fontsize=7.5, bold=True)

    # Self-reflection indicator
    ax.annotate("", xy=(-0.55, -1.45), xytext=(-0.55, -1.0),
                arrowprops=dict(arrowstyle="->", color=c_loop, lw=1.4,
                                connectionstyle="arc3,rad=-0.6"))
    ax.text(-0.1, -1.2, "×3", fontsize=6, color=c_loop, weight="bold")

    _box(-2.2, -2.4, 3.2, 0.55, "Cypher Gen + Healing → Upsert", c_builder_box, fontsize=7.5)

    # Arrows inside builder
    for y_top, y_bot in [(1.0, 0.1), (0.1, -0.8), (-0.8, -1.7), (-1.7, -2.4)]:
        _arrow(-2.2, y_top - 0.275, -2.2, y_bot + 0.275, color="#8D6E63", lw=1.0)

    # Input arrows to builder
    _arrow(-6 + 1.3, 2.0, -2.2 - 1.6, 1.0 + 0.15, color=c_edge, lw=1.2)
    _arrow(-6 + 1.3, 0.8, -2.2 - 1.6, 0.1 + 0.0, color=c_edge, lw=1.2)

    # ══════════════════════════════════════════════════════
    # CENTER — Neo4j Knowledge Graph
    # ══════════════════════════════════════════════════════
    kg_rect = mpatches.FancyBboxPatch(
        (0.5, -1.3), 2.6, 2.6,
        boxstyle="round,pad=0.15", facecolor=c_kg, edgecolor="#455A64", linewidth=2.5
    )
    ax.add_patch(kg_rect)
    ax.text(1.8, 0.45, "Neo4j", ha="center", va="center",
            fontsize=11, weight="bold", color="white")
    ax.text(1.8, -0.1, "Knowledge\nGraph", ha="center", va="center",
            fontsize=9, color="#B0BEC5", linespacing=1.3)
    ax.text(1.8, -0.85, "6 labels · 5 rels\n3 vector indexes", ha="center", va="center",
            fontsize=6.5, color="#78909C", linespacing=1.3)

    # Builder → KG (write)
    _arrow(-0.6, -1.7, 0.5, -0.3, color="#E65100", lw=2.0)
    ax.text(-0.3, -1.25, "WRITE", ha="center", va="center",
            fontsize=7, weight="bold", color="#E65100",
            bbox=dict(boxstyle="round,pad=0.1", facecolor="white", edgecolor="#E65100", alpha=0.9))

    # KG → Query (read)
    _arrow(3.1, -0.3, 4.1, -1.7, color="#2E7D32", lw=2.0)
    ax.text(3.9, -1.25, "READ", ha="center", va="center",
            fontsize=7, weight="bold", color="#2E7D32",
            bbox=dict(boxstyle="round,pad=0.1", facecolor="white", edgecolor="#2E7D32", alpha=0.9))

    # ══════════════════════════════════════════════════════
    # CENTER-RIGHT — Query Graph (simplified)
    # ══════════════════════════════════════════════════════
    query_rect = mpatches.FancyBboxPatch(
        (3.8, -2.8), 4.0, 5.5,
        boxstyle="round,pad=0.2", facecolor=c_query, edgecolor="#2E7D32",
        linewidth=2, alpha=0.35
    )
    ax.add_patch(query_rect)
    ax.text(5.8, 2.3, "Query Graph", ha="center", va="center",
            fontsize=11, weight="bold", color="#1B5E20")
    ax.text(5.8, 1.8, "(Read path — real-time)", ha="center", va="center",
            fontsize=7, color="#1B5E20", style="italic")

    _box(5.8, 1.0, 3.2, 0.55, "Hybrid Retrieval (Vec+BM25+Graph)", c_query_box, fontsize=7.5)
    _box(5.8, 0.1, 3.2, 0.55, "Cross-Encoder Reranking", c_query_box, fontsize=7.5)
    _box(5.8, -0.8, 3.2, 0.55, "Quality Gate + Context Distillation", c_query_box, fontsize=7.5)
    _box(5.8, -1.7, 3.2, 0.55, "Answer Generation", c_query_box, fontsize=7.5, bold=True)
    _box(5.8, -2.4, 3.2, 0.55, "Hallucination Grading (Self-RAG)", c_query_box, fontsize=7.5, bold=True)

    # Self-reflection indicator
    ax.annotate("", xy=(7.45, -1.45), xytext=(7.45, -2.15),
                arrowprops=dict(arrowstyle="->", color=c_loop, lw=1.4,
                                connectionstyle="arc3,rad=-0.6"))
    ax.text(7.0, -1.8, "×3", fontsize=6, color=c_loop, weight="bold")

    # Arrows inside query
    for y_top, y_bot in [(1.0, 0.1), (0.1, -0.8), (-0.8, -1.7), (-1.7, -2.4)]:
        _arrow(5.8, y_top - 0.275, 5.8, y_bot + 0.275, color="#558B2F", lw=1.0)

    # ══════════════════════════════════════════════════════
    # RIGHT — Output + Question
    # ══════════════════════════════════════════════════════
    # Question input (top-right)
    ax.text(5.8, 3.0, "Natural Language\nQuestion", ha="center", va="center", fontsize=8,
            bbox=dict(boxstyle="round", facecolor=c_input, edgecolor="#90CAF9", linewidth=1.5))
    _arrow(5.8, 3.0 - 0.3, 5.8, 1.0 + 0.275)

    # Output (bottom-right)
    out_rect = mpatches.FancyBboxPatch(
        (4.3, -4.3), 3.0, 0.8,
        boxstyle="round,pad=0.12", facecolor=c_output, edgecolor="#455A64", linewidth=2
    )
    ax.add_patch(out_rect)
    ax.text(5.8, -3.9, "Grounded Answer\n+ Sources", ha="center", va="center",
            fontsize=9, weight="bold", color="white", linespacing=1.3)
    _arrow(5.8, -2.4 - 0.275, 5.8, -3.9 + 0.4)

    # ══════════════════════════════════════════════════════
    # BOTTOM CENTER — CQRS label
    # ══════════════════════════════════════════════════════
    ax.text(1.8, -4.8, "CQRS Separation: Builder writes, Query reads, Neo4j stores",
            ha="center", va="center", fontsize=8, color="#546E7A", style="italic",
            bbox=dict(boxstyle="round,pad=0.2", facecolor="#ECEFF1", edgecolor="#B0BEC5", alpha=0.7))

    # ── Title ──
    ax.set_title("SemanticMesh — System Overview", fontsize=14, weight="bold", pad=18)

    # ── Legend ──
    legend_elements = [
        mpatches.Patch(facecolor=c_input, edgecolor="#90CAF9", label="Input / Question"),
        mpatches.Patch(facecolor=c_builder_box, edgecolor="#37474F", label="Builder Graph (Write)"),
        mpatches.Patch(facecolor=c_kg, edgecolor="#455A64", label="Neo4j Knowledge Graph"),
        mpatches.Patch(facecolor=c_query_box, edgecolor="#37474F", label="Query Graph (Read)"),
        mpatches.Patch(facecolor=c_loop, edgecolor=c_loop, label="Self-Reflection Loop"),
    ]
    ax.legend(handles=legend_elements, loc="lower left", fontsize=7.5, framealpha=0.9)

    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "system_overview.png", dpi=150, bbox_inches="tight",
                facecolor="white", edgecolor="none")
    plt.close(fig)
    print(f"  ✓ {OUTPUT_DIR / 'system_overview.png'}")


if __name__ == "__main__":
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print("Generating architecture diagrams...")
    _draw_builder_graph()
    _draw_query_graph()
    _draw_system_overview()
    print("Done.")
