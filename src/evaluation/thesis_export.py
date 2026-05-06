"""Thesis-ready CSV and plot generation for pipeline runs and ablation studies.

Generates:
  - CSV files with per-question results, per-dataset summaries, per-study aggregates
  - Matplotlib/Seaborn plots: heatmaps, bar charts, radar charts, box plots, etc.
  - All outputs saved under outputs/thesis/ (or a configurable directory)

Can be called standalone or integrated into run_pipeline / generate_ablation_report.
"""

from __future__ import annotations

import csv
import json
import statistics
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")  # non-interactive backend for headless generation

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# ── Styling ──────────────────────────────────────────────────────────────────────

# Academic-friendly defaults
sns.set_theme(style="whitegrid", font_scale=1.1, rc={
    "figure.dpi": 150,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "axes.titlesize": 13,
    "axes.labelsize": 11,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "legend.fontsize": 9,
    "figure.figsize": (10, 6),
    "font.family": "serif",
})

PALETTE = sns.color_palette("Set2", 21)

DATASETS = [
    "01_basics_ecommerce",
    "02_intermediate_finance",
    "03_advanced_healthcare",
    "04_complex_manufacturing",
    "05_edgecases_incomplete",
    "06_edgecases_legacy",
]

DS_SHORT = {
    "01_basics_ecommerce": "DS01",
    "02_intermediate_finance": "DS02",
    "03_advanced_healthcare": "DS03",
    "04_complex_manufacturing": "DS04",
    "05_edgecases_incomplete": "DS05",
    "06_edgecases_legacy": "DS06",
}

STUDY_IDS = [f"AB-{i:02d}" for i in range(21)]

SCORE_DIMS = ["overall", "builder", "retrieval", "answer", "pipeline", "ablation"]
RAW_METRICS = ["grounded_rate", "avg_gt_coverage", "avg_top_score", "triplets", "entities"]


# ── CSV Exports ──────────────────────────────────────────────────────────────────


def export_run_csv(summary: dict[str, Any], output_dir: Path) -> Path:
    """Export a single run's per-question results to CSV."""
    output_dir.mkdir(parents=True, exist_ok=True)
    study_id = summary.get("study_id", "unknown")
    dataset_id = summary.get("dataset_id", "unknown")
    csv_path = output_dir / f"{study_id}_{dataset_id}_per_question.csv"

    per_question = summary.get("per_question", [])
    if not per_question:
        return csv_path

    fieldnames = [
        "study_id", "dataset_id", "run_tag", "query_id", "question",
        "query_type", "difficulty", "grounded", "gt_coverage",
        "retrieval_quality_score", "retrieval_chunk_count",
        "retrieval_gate_decision", "context_sufficiency",
        "grader_rejection_count", "grader_consistency_valid",
        "expected_answer", "generated_answer",
    ]

    # Add RAGAS fields if present
    sample_ragas = per_question[0].get("ragas_scores") if per_question else None
    ragas_keys = []
    if sample_ragas:
        ragas_keys = sorted(sample_ragas.keys())
        fieldnames.extend(f"ragas_{k}" for k in ragas_keys)

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for pq in per_question:
            row = {
                "study_id": study_id,
                "dataset_id": dataset_id,
                "run_tag": summary.get("run_tag", ""),
                "query_id": pq.get("query_id", ""),
                "question": pq.get("question", ""),
                "query_type": pq.get("query_type", ""),
                "difficulty": pq.get("difficulty", ""),
                "grounded": pq.get("grounded", False),
                "gt_coverage": pq.get("gt_coverage"),  # None when expected_sources absent
                "retrieval_quality_score": pq.get("retrieval_quality_score", 0.0),
                "retrieval_chunk_count": pq.get("retrieval_chunk_count", 0),
                "retrieval_gate_decision": pq.get("retrieval_gate_decision", ""),
                "context_sufficiency": pq.get("context_sufficiency", ""),
                "grader_rejection_count": pq.get("grader_rejection_count", 0),
                "grader_consistency_valid": pq.get("grader_consistency_valid", True),
                "expected_answer": pq.get("expected_answer", ""),
                "generated_answer": pq.get("generated_answer", ""),
            }
            ragas = pq.get("ragas_scores") or {}
            for k in ragas_keys:
                row[f"ragas_{k}"] = ragas.get(k, "")
            writer.writerow(row)

    return csv_path


def export_run_summary_csv(summary: dict[str, Any], output_dir: Path) -> Path:
    """Export single-run aggregate metrics to a one-row CSV."""
    output_dir.mkdir(parents=True, exist_ok=True)
    study_id = summary.get("study_id", "unknown")
    dataset_id = summary.get("dataset_id", "unknown")
    csv_path = output_dir / f"{study_id}_{dataset_id}_summary.csv"

    cfg = summary.get("config", {})
    bld = summary.get("builder", {})
    qry = summary.get("query", {})
    ragas = summary.get("ragas") or {}

    row = {
        "study_id": study_id,
        "dataset_id": dataset_id,
        "run_tag": summary.get("run_tag", ""),
        "timestamp": summary.get("timestamp", ""),
        # Config
        "extraction_mode": cfg.get("extraction_mode", ""),
        "reasoning_model": cfg.get("reasoning_model", ""),
        "embedding_model": cfg.get("embedding_model", ""),
        "retrieval_mode": cfg.get("retrieval_mode", ""),
        "enable_reranker": cfg.get("enable_reranker", ""),
        "reranker_top_k": cfg.get("reranker_top_k", ""),
        "chunk_size": cfg.get("chunk_size", ""),
        "chunk_overlap": cfg.get("chunk_overlap", ""),
        "er_similarity_threshold": cfg.get("er_similarity_threshold", ""),
        # Builder
        "triplets": bld.get("triplets", 0),
        "entities": bld.get("entities", 0),
        "tables_parsed": bld.get("tables_parsed", 0),
        "tables_completed": bld.get("tables_completed", 0),
        "builder_elapsed_s": bld.get("elapsed_s", ""),
        # Query
        "total_questions": qry.get("total_questions", 0),
        "grounded_count": qry.get("grounded_count", 0),
        "grounded_rate": qry.get("grounded_rate", 0),
        "avg_gt_coverage": qry.get("avg_gt_coverage", 0),
        "avg_top_score": qry.get("avg_top_score", 0),
        "avg_chunk_count": qry.get("avg_chunk_count", 0),
        "abstained_count": qry.get("abstained_count", 0),
    }
    # RAGAS
    if ragas and "error" not in ragas:
        for k, v in ragas.items():
            row[f"ragas_{k}"] = v

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(row.keys()))
        writer.writeheader()
        writer.writerow(row)

    return csv_path


def export_run_plots(summary: dict[str, Any], output_dir: Path) -> list[Path]:
    """Generate per-run plots for a single pipeline execution."""
    output_dir.mkdir(parents=True, exist_ok=True)
    study_id = summary.get("study_id", "unknown")
    dataset_id = summary.get("dataset_id", "unknown")
    prefix = f"{study_id}_{dataset_id}"
    pq = summary.get("per_question", [])
    paths: list[Path] = []

    if not pq:
        return paths

    # ── 1. Per-question GT coverage bar chart ──
    fig, ax = plt.subplots(figsize=(12, 5))
    qids = [r.get("query_id", f"Q{i}") for i, r in enumerate(pq)]
    coverages = [r.get("gt_coverage") for r in pq]  # may contain None
    # For bars: None → 0 (visually absent); distinct colour signals unmeasured
    bar_coverages = [c if c is not None else 0.0 for c in coverages]
    has_null_coverage = any(c is None for c in coverages)
    colors = ["#2ecc71" if r.get("grounded") else "#e74c3c" for r in pq]
    ax.bar(qids, bar_coverages, color=colors, edgecolor="white", linewidth=0.5)
    ax.set_ylabel("GT Coverage")
    ax.set_title(f"{study_id} / {DS_SHORT.get(dataset_id, dataset_id)} — Per-Question GT Coverage")
    ax.set_ylim(0, 1.05)
    ax.axhline(y=1.0, color="gray", linestyle="--", alpha=0.5)
    ax.tick_params(axis="x", rotation=45)
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor="#2ecc71", label="Grounded"),
                       Patch(facecolor="#e74c3c", label="Ungrounded")]
    if has_null_coverage:
        legend_elements.append(Patch(facecolor="none", edgecolor="gray", label="GT N/A (0 shown)"))
    ax.legend(handles=legend_elements, loc="lower right")
    p = output_dir / f"{prefix}_gt_coverage_bar.png"
    fig.savefig(p)
    plt.close(fig)
    paths.append(p)

    # ── 2. Retrieval quality score distribution ──
    scores = [r.get("retrieval_quality_score", 0) for r in pq]
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(scores, bins=15, kde=True, ax=ax, color=PALETTE[0])
    ax.set_xlabel("Retrieval Quality Score")
    ax.set_ylabel("Count")
    ax.set_title(f"{study_id} / {DS_SHORT.get(dataset_id, dataset_id)} — Retrieval Score Distribution")
    p = output_dir / f"{prefix}_retrieval_score_dist.png"
    fig.savefig(p)
    plt.close(fig)
    paths.append(p)

    # ── 3. Difficulty vs GT coverage box plot (if difficulty info present) ──
    difficulties = [r.get("difficulty", "unknown") for r in pq]
    unique_diffs = sorted(set(difficulties))
    # Only draw boxplot when we have measured gt_coverage values
    measured_coverages = [c for c in coverages if c is not None]
    if len(unique_diffs) > 1 and measured_coverages:
        import pandas as pd
        df_rows = [
            {"difficulty": d, "gt_coverage": c}
            for d, c in zip(difficulties, coverages)
            if c is not None
        ]
        df = pd.DataFrame(df_rows)
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.boxplot(data=df, x="difficulty", y="gt_coverage", ax=ax, palette="Set2",
                    order=["easy", "medium", "hard"] if set(unique_diffs) <= {"easy", "medium", "hard", "unknown"} else unique_diffs)
        ax.set_title(f"{study_id} / {DS_SHORT.get(dataset_id, dataset_id)} — GT Coverage by Difficulty")
        ax.set_ylim(0, 1.05)
        p = output_dir / f"{prefix}_coverage_by_difficulty.png"
        fig.savefig(p)
        plt.close(fig)
        paths.append(p)

    # ── 4. RAGAS radar chart (if available) ──
    ragas = summary.get("ragas") or {}
    if ragas and "error" not in ragas:
        ragas_keys = ["faithfulness", "answer_relevancy", "context_precision", "context_recall"]
        ragas_vals = [ragas.get(k, 0) for k in ragas_keys]
        if any(v > 0 for v in ragas_vals):
            fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
            angles = np.linspace(0, 2 * np.pi, len(ragas_keys), endpoint=False).tolist()
            ragas_vals_closed = ragas_vals + [ragas_vals[0]]
            angles_closed = angles + [angles[0]]
            ax.plot(angles_closed, ragas_vals_closed, "o-", linewidth=2, color=PALETTE[1])
            ax.fill(angles_closed, ragas_vals_closed, alpha=0.25, color=PALETTE[1])
            ax.set_thetagrids(np.degrees(angles), ragas_keys)
            ax.set_ylim(0, 1)
            ax.set_title(f"{study_id} / {DS_SHORT.get(dataset_id, dataset_id)} — RAGAS Radar", pad=20)
            p = output_dir / f"{prefix}_ragas_radar.png"
            fig.savefig(p)
            plt.close(fig)
            paths.append(p)

    return paths


# ── Ablation-Level Exports ───────────────────────────────────────────────────────


def export_ablation_master_csv(
    all_scores: dict[str, dict[str, dict[str, Any]]],
    output_dir: Path,
) -> list[Path]:
    """Export ablation-wide CSVs from all_scores_full.json data.

    Returns list of created CSV paths.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []

    # ── 1. Flat per-study-dataset CSV ──
    flat_path = output_dir / "ablation_all_scores.csv"
    flat_fields = [
        "study_id", "dataset_id",
        "overall", "builder", "retrieval", "answer", "pipeline", "ablation",
        "grounded_rate", "avg_gt_coverage", "avg_top_score",
        "triplets", "entities", "tables_done", "tables_parsed",
    ]
    with open(flat_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=flat_fields, extrasaction="ignore")
        writer.writeheader()
        for study_id in sorted(all_scores.keys()):
            for ds_id in DATASETS:
                v = all_scores.get(study_id, {}).get(ds_id)
                if not v:
                    continue
                row = {"study_id": study_id, "dataset_id": ds_id}
                row.update(v)
                writer.writerow(row)
    paths.append(flat_path)

    # ── 2. Per-study aggregated CSV ──
    agg_path = output_dir / "ablation_study_averages.csv"
    agg_fields = [
        "study_id", "n_datasets",
        "overall_mean", "overall_std",
        "builder_mean", "retrieval_mean", "answer_mean", "pipeline_mean",
        "grounded_rate_mean", "avg_gt_coverage_mean", "avg_top_score_mean",
        "triplets_mean", "entities_mean",
    ]
    with open(agg_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=agg_fields)
        writer.writeheader()
        for study_id in sorted(all_scores.keys()):
            vals = list(all_scores[study_id].values())
            if not vals:
                continue
            n = len(vals)

            def _mean(k: str) -> float:
                s = [v.get(k, 0) or 0 for v in vals]
                return sum(s) / n if n else 0

            overalls = [v.get("overall", 0) or 0 for v in vals]
            writer.writerow({
                "study_id": study_id,
                "n_datasets": n,
                "overall_mean": round(_mean("overall"), 4),
                "overall_std": round(statistics.stdev(overalls), 4) if n > 1 else 0,
                "builder_mean": round(_mean("builder"), 4),
                "retrieval_mean": round(_mean("retrieval"), 4),
                "answer_mean": round(_mean("answer"), 4),
                "pipeline_mean": round(_mean("pipeline"), 4),
                "grounded_rate_mean": round(_mean("grounded_rate"), 4),
                "avg_gt_coverage_mean": round(_mean("avg_gt_coverage"), 4),
                "avg_top_score_mean": round(_mean("avg_top_score"), 4),
                "triplets_mean": round(_mean("triplets"), 1),
                "entities_mean": round(_mean("entities"), 1),
            })
    paths.append(agg_path)

    # ── 3. Per-dataset aggregated CSV ──
    ds_path = output_dir / "ablation_dataset_averages.csv"
    ds_fields = [
        "dataset_id", "n_studies",
        "overall_mean", "overall_std",
        "builder_mean", "retrieval_mean", "answer_mean", "pipeline_mean",
        "grounded_rate_mean", "avg_gt_coverage_mean",
    ]
    with open(ds_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=ds_fields)
        writer.writeheader()
        for ds_id in DATASETS:
            vals = [
                all_scores[sid][ds_id]
                for sid in all_scores
                if ds_id in all_scores[sid] and all_scores[sid][ds_id]
            ]
            if not vals:
                continue
            n = len(vals)

            def _mean(k: str) -> float:
                s = [v.get(k, 0) or 0 for v in vals]
                return sum(s) / n if n else 0

            overalls = [v.get("overall", 0) or 0 for v in vals]
            writer.writerow({
                "dataset_id": ds_id,
                "n_studies": n,
                "overall_mean": round(_mean("overall"), 4),
                "overall_std": round(statistics.stdev(overalls), 4) if n > 1 else 0,
                "builder_mean": round(_mean("builder"), 4),
                "retrieval_mean": round(_mean("retrieval"), 4),
                "answer_mean": round(_mean("answer"), 4),
                "pipeline_mean": round(_mean("pipeline"), 4),
                "grounded_rate_mean": round(_mean("grounded_rate"), 4),
                "avg_gt_coverage_mean": round(_mean("avg_gt_coverage"), 4),
            })
    paths.append(ds_path)

    return paths


def export_ablation_plots(
    all_scores: dict[str, dict[str, dict[str, Any]]],
    output_dir: Path,
    ablation_desc: dict[str, dict[str, str]] | None = None,
) -> list[Path]:
    """Generate ablation-wide thesis-ready plots.

    Returns list of created image paths.
    """
    import pandas as pd

    output_dir.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []

    # Build flat DataFrame
    rows = []
    for study_id in sorted(all_scores.keys()):
        for ds_id in DATASETS:
            v = all_scores.get(study_id, {}).get(ds_id)
            if not v:
                continue
            row = {"study_id": study_id, "dataset_id": ds_id, "ds_short": DS_SHORT.get(ds_id, ds_id)}
            row.update(v)
            rows.append(row)

    if not rows:
        return paths

    df = pd.DataFrame(rows)

    # Ensure studies are ordered
    study_order = [s for s in STUDY_IDS if s in df["study_id"].unique()]
    df["study_id"] = pd.Categorical(df["study_id"], categories=study_order, ordered=True)

    # ── 1. Overall score heatmap (study × dataset) ──
    pivot = df.pivot_table(index="study_id", columns="ds_short", values="overall", aggfunc="mean")
    ds_col_order = [DS_SHORT[d] for d in DATASETS if DS_SHORT[d] in pivot.columns]
    pivot = pivot[ds_col_order]

    fig, ax = plt.subplots(figsize=(10, 9))
    sns.heatmap(
        pivot, annot=True, fmt=".2f", cmap="RdYlGn", center=3.5,
        vmin=1.5, vmax=5.0, linewidths=0.5, ax=ax,
        cbar_kws={"label": "AI-Judge Overall Score"},
    )
    ax.set_title("AI-Judge Overall Scores — Study × Dataset Heatmap")
    ax.set_ylabel("Ablation Study")
    ax.set_xlabel("Dataset")
    p = output_dir / "heatmap_overall_scores.png"
    fig.savefig(p)
    plt.close(fig)
    paths.append(p)

    # ── 2. Per-dimension heatmaps ──
    for dim in ["builder", "retrieval", "answer", "pipeline"]:
        if dim not in df.columns:
            continue
        pivot_dim = df.pivot_table(index="study_id", columns="ds_short", values=dim, aggfunc="mean")
        pivot_dim = pivot_dim[[c for c in ds_col_order if c in pivot_dim.columns]]
        fig, ax = plt.subplots(figsize=(10, 9))
        sns.heatmap(
            pivot_dim, annot=True, fmt=".1f", cmap="RdYlGn", center=3.0,
            vmin=1.0, vmax=5.0, linewidths=0.5, ax=ax,
            cbar_kws={"label": f"{dim.title()} Score"},
        )
        ax.set_title(f"AI-Judge {dim.title()} Scores — Study × Dataset")
        ax.set_ylabel("Ablation Study")
        ax.set_xlabel("Dataset")
        p = output_dir / f"heatmap_{dim}_scores.png"
        fig.savefig(p)
        plt.close(fig)
        paths.append(p)

    # ── 3. Study-averaged overall score bar chart with error bars ──
    study_agg = df.groupby("study_id", observed=True)["overall"].agg(["mean", "std"]).reset_index()
    study_agg = study_agg.sort_values("study_id")

    baseline_mean = study_agg.loc[study_agg["study_id"] == "AB-00", "mean"].values
    baseline_val = baseline_mean[0] if len(baseline_mean) > 0 else 0

    fig, ax = plt.subplots(figsize=(14, 6))
    colors_bar = ["#3498db" if s == "AB-00" else ("#2ecc71" if m >= baseline_val else "#e74c3c")
                  for s, m in zip(study_agg["study_id"], study_agg["mean"])]
    ax.bar(
        study_agg["study_id"].astype(str), study_agg["mean"],
        yerr=study_agg["std"].fillna(0), capsize=3,
        color=colors_bar, edgecolor="white", linewidth=0.5,
    )
    ax.axhline(y=baseline_val, color="#3498db", linestyle="--", alpha=0.7, label=f"Baseline ({baseline_val:.2f})")
    ax.set_ylabel("Overall Score (AI-Judge)")
    ax.set_title("Ablation Studies — Average Overall Score (±1 SD)")
    ax.set_ylim(0, 5.2)
    ax.tick_params(axis="x", rotation=45)
    ax.legend()
    p = output_dir / "bar_overall_scores.png"
    fig.savefig(p)
    plt.close(fig)
    paths.append(p)

    # ── 4. Delta vs baseline bar chart ──
    study_agg["delta"] = study_agg["mean"] - baseline_val
    fig, ax = plt.subplots(figsize=(14, 5))
    colors_delta = ["#2ecc71" if d >= 0 else "#e74c3c" for d in study_agg["delta"]]
    ax.bar(
        study_agg["study_id"].astype(str), study_agg["delta"],
        color=colors_delta, edgecolor="white", linewidth=0.5,
    )
    ax.axhline(y=0, color="black", linewidth=0.8)
    ax.set_ylabel("Δ Overall Score vs. Baseline (AB-00)")
    ax.set_title("Ablation Impact — Delta from Baseline")
    ax.tick_params(axis="x", rotation=45)
    p = output_dir / "bar_delta_vs_baseline.png"
    fig.savefig(p)
    plt.close(fig)
    paths.append(p)

    # ── 5. Grouped bar chart: score dimensions per study ──
    dims = ["builder", "retrieval", "answer", "pipeline"]
    avail_dims = [d for d in dims if d in df.columns]
    if avail_dims:
        dim_agg = df.groupby("study_id", observed=True)[avail_dims].mean().reset_index()
        dim_agg = dim_agg.sort_values("study_id")
        x = np.arange(len(dim_agg))
        width = 0.18
        fig, ax = plt.subplots(figsize=(16, 6))
        for i, dim in enumerate(avail_dims):
            ax.bar(x + i * width, dim_agg[dim], width, label=dim.title(), color=PALETTE[i])
        ax.set_xticks(x + width * (len(avail_dims) - 1) / 2)
        ax.set_xticklabels(dim_agg["study_id"].astype(str), rotation=45, ha="right")
        ax.set_ylabel("Score (1–5)")
        ax.set_title("Score Dimensions per Ablation Study")
        ax.set_ylim(0, 5.5)
        ax.legend(loc="upper right")
        p = output_dir / "bar_dimensions_grouped.png"
        fig.savefig(p)
        plt.close(fig)
        paths.append(p)

    # ── 6. Raw metrics: grounded_rate and gt_coverage per study ──
    for metric, label, ylim in [
        ("grounded_rate", "Grounded Rate", (0, 1.05)),
        ("avg_gt_coverage", "Avg GT Coverage", (0, 1.05)),
        ("avg_top_score", "Avg Top Score", None),
    ]:
        if metric not in df.columns:
            continue
        metric_agg = df.groupby("study_id", observed=True)[metric].agg(["mean", "std"]).reset_index()
        metric_agg = metric_agg.sort_values("study_id")
        fig, ax = plt.subplots(figsize=(14, 5))
        ax.bar(
            metric_agg["study_id"].astype(str), metric_agg["mean"],
            yerr=metric_agg["std"].fillna(0), capsize=3,
            color=PALETTE[3], edgecolor="white",
        )
        ax.set_ylabel(label)
        ax.set_title(f"{label} per Ablation Study (±1 SD)")
        if ylim:
            ax.set_ylim(*ylim)
        ax.tick_params(axis="x", rotation=45)
        p = output_dir / f"bar_{metric}.png"
        fig.savefig(p)
        plt.close(fig)
        paths.append(p)

    # ── 7. Box plots: overall score distribution per study ──
    fig, ax = plt.subplots(figsize=(14, 6))
    sns.boxplot(
        data=df, x="study_id", y="overall", ax=ax,
        palette="Set2", order=study_order,
    )
    ax.axhline(y=baseline_val, color="#3498db", linestyle="--", alpha=0.7, label="Baseline mean")
    ax.set_ylabel("Overall Score")
    ax.set_title("Overall Score Distribution per Study (across 6 datasets)")
    ax.tick_params(axis="x", rotation=45)
    ax.legend()
    p = output_dir / "box_overall_per_study.png"
    fig.savefig(p)
    plt.close(fig)
    paths.append(p)

    # ── 8. Box plot: overall per dataset (across studies) ──
    fig, ax = plt.subplots(figsize=(10, 6))
    ds_order = [DS_SHORT[d] for d in DATASETS if DS_SHORT[d] in df["ds_short"].unique()]
    sns.boxplot(data=df, x="ds_short", y="overall", ax=ax, palette="Set3", order=ds_order)
    ax.set_ylabel("Overall Score")
    ax.set_title("Overall Score Distribution per Dataset (across 21 studies)")
    ax.set_xlabel("Dataset")
    p = output_dir / "box_overall_per_dataset.png"
    fig.savefig(p)
    plt.close(fig)
    paths.append(p)

    # ── 9. Radar/spider chart for grouped ablation themes ──
    groups = {
        "Retrieval Mode": ["AB-00", "AB-01", "AB-02", "AB-03"],
        "Reranker Pool": ["AB-00", "AB-04", "AB-05"],
        "Chunk Size": ["AB-00", "AB-06", "AB-07", "AB-08"],
        "Extraction Tokens": ["AB-00", "AB-09", "AB-10"],
        "ER Threshold": ["AB-00", "AB-11", "AB-12"],
        "Builder Components": ["AB-00", "AB-15", "AB-16", "AB-19"],
    }
    radar_dims = ["retrieval", "answer", "pipeline"]
    radar_dims = [d for d in radar_dims if d in df.columns]

    if radar_dims:
        for group_name, group_studies in groups.items():
            avail = [s for s in group_studies if s in df["study_id"].cat.categories]
            if len(avail) < 2:
                continue

            fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True))
            angles = np.linspace(0, 2 * np.pi, len(radar_dims), endpoint=False).tolist()
            angles_closed = angles + [angles[0]]

            for idx, sid in enumerate(avail):
                sub = df[df["study_id"] == sid]
                vals = [sub[d].mean() for d in radar_dims]
                vals_closed = vals + [vals[0]]
                ax.plot(angles_closed, vals_closed, "o-", linewidth=2, label=sid, color=PALETTE[idx])
                ax.fill(angles_closed, vals_closed, alpha=0.1, color=PALETTE[idx])

            ax.set_thetagrids(np.degrees(angles), [d.title() for d in radar_dims])
            ax.set_ylim(0, 5.5)
            ax.set_title(f"Ablation Group: {group_name}", pad=20)
            ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1))
            p = output_dir / f"radar_{group_name.lower().replace(' ', '_')}.png"
            fig.savefig(p)
            plt.close(fig)
            paths.append(p)

    # ── 10. Triplets & Entities scatter ──
    if "triplets" in df.columns and "entities" in df.columns:
        fig, ax = plt.subplots(figsize=(10, 6))
        scatter_df = df[df["triplets"] > 0].copy()
        if not scatter_df.empty:
            sns.scatterplot(
                data=scatter_df, x="triplets", y="entities",
                hue="study_id", style="ds_short", s=100, ax=ax, palette="tab20",
            )
            ax.set_xlabel("Triplets Extracted")
            ax.set_ylabel("Entities Resolved")
            ax.set_title("KG Size: Triplets vs Entities per Run")
            ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left", fontsize=7)
            p = output_dir / "scatter_triplets_entities.png"
            fig.savefig(p)
            plt.close(fig)
            paths.append(p)

    # ── 11. Correlation heatmap of all numeric metrics ──
    numeric_cols = ["overall", "builder", "retrieval", "answer", "pipeline",
                    "grounded_rate", "avg_gt_coverage", "avg_top_score", "triplets", "entities"]
    numeric_cols = [c for c in numeric_cols if c in df.columns]
    if len(numeric_cols) >= 4:
        corr = df[numeric_cols].corr()
        fig, ax = plt.subplots(figsize=(10, 8))
        mask = np.triu(np.ones_like(corr, dtype=bool))
        sns.heatmap(
            corr, mask=mask, annot=True, fmt=".2f", cmap="coolwarm",
            center=0, square=True, linewidths=0.5, ax=ax,
        )
        ax.set_title("Metric Correlation Matrix")
        p = output_dir / "heatmap_correlation.png"
        fig.savefig(p)
        plt.close(fig)
        paths.append(p)

    # ── 12. Component importance ranking (horizontal bar) ──
    if baseline_val > 0:
        study_means = df.groupby("study_id", observed=True)["overall"].mean()
        deltas = {sid: study_means.get(sid, 0) - baseline_val for sid in study_order if sid != "AB-00"}
        if deltas:
            sorted_deltas = sorted(deltas.items(), key=lambda x: x[1])
            fig, ax = plt.subplots(figsize=(10, 8))
            studies_sorted = [s for s, _ in sorted_deltas]
            delta_vals = [d for _, d in sorted_deltas]
            colors_h = ["#2ecc71" if d >= 0 else "#e74c3c" for d in delta_vals]

            labels = studies_sorted
            if ablation_desc:
                labels = [f"{s}: {ablation_desc.get(s, {}).get('title', s)[:35]}" for s in studies_sorted]

            ax.barh(labels, delta_vals, color=colors_h, edgecolor="white")
            ax.axvline(x=0, color="black", linewidth=0.8)
            ax.set_xlabel("Δ Overall Score vs. Baseline")
            ax.set_title("Component Importance Ranking (by Impact on Overall Score)")
            p = output_dir / "bar_component_importance.png"
            fig.savefig(p)
            plt.close(fig)
            paths.append(p)

    return paths


# ── Convenience: All-in-One for Ablation ──────────────────────────────────────


def generate_all_thesis_artifacts(
    all_scores_path: Path,
    output_dir: Path | None = None,
    ablation_desc: dict | None = None,
) -> dict[str, list[Path]]:
    """Generate all thesis CSVs and plots from all_scores_full.json.

    Returns a dict with keys 'csv' and 'plots', each containing list of paths.
    """
    if output_dir is None:
        output_dir = all_scores_path.parent / "thesis"
    output_dir.mkdir(parents=True, exist_ok=True)

    all_scores = json.loads(all_scores_path.read_text(encoding="utf-8"))

    csv_dir = output_dir / "csv"
    plot_dir = output_dir / "plots"

    csv_paths = export_ablation_master_csv(all_scores, csv_dir)
    plot_paths = export_ablation_plots(all_scores, plot_dir, ablation_desc=ablation_desc)

    print(f"\n{'='*60}")
    print("  THESIS ARTIFACTS GENERATED")
    print(f"{'='*60}")
    print(f"  CSVs:  {len(csv_paths)} files in {csv_dir}")
    for p in csv_paths:
        print(f"    - {p.name}")
    print(f"  Plots: {len(plot_paths)} files in {plot_dir}")
    for p in plot_paths:
        print(f"    - {p.name}")
    print(f"{'='*60}\n")

    return {"csv": csv_paths, "plots": plot_paths}
