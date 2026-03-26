"""Ablation Studies REST API — /api/v1/ablation/..."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from fastapi import APIRouter, BackgroundTasks, HTTPException

from src.api.jobs import create_job, get_job, list_jobs, set_done, set_failed, set_running
from src.api.models import (
    AblationJobResponse,
    AblationMatrixEntry,
    AblationResultResponse,
    AblationRunRequest,
)
from src.evaluation.ablation_runner import ABLATION_MATRIX, _settings_override

router = APIRouter(prefix="/ablation", tags=["Ablation Studies"])

# ── Helpers ───────────────────────────────────────────────────────────────────

_ROOT = Path(__file__).parent.parent.parent  # repo root


def _fixtures_dir() -> Path:
    return _ROOT / "tests" / "fixtures"


def _build_env_overrides(req: AblationRunRequest) -> dict[str, str]:
    """Translate non-None hyperparameter fields in the request to env vars."""
    mapping: dict[str, Any] = {
        "RETRIEVAL_MODE": req.retrieval_mode,
        "ENABLE_RERANKER": req.enable_reranker,
        "RERANKER_TOP_K": req.reranker_top_k,
        "ENABLE_HALLUCINATION_GRADER": req.enable_hallucination_grader,
        "ENABLE_CYPHER_HEALING": req.enable_cypher_healing,
        "ENABLE_CRITIC_VALIDATION": req.enable_critic_validation,
        "ENABLE_SCHEMA_ENRICHMENT": req.enable_schema_enrichment,
        "CHUNK_SIZE": req.chunk_size,
        "CHUNK_OVERLAP": req.chunk_overlap,
        "PARENT_CHUNK_SIZE": req.parent_chunk_size,
        "ER_SIMILARITY_THRESHOLD": req.er_similarity_threshold,
        "ER_BLOCKING_TOP_K": req.er_blocking_top_k,
        "CONFIDENCE_THRESHOLD": req.confidence_threshold,
        "RETRIEVAL_VECTOR_TOP_K": req.retrieval_vector_top_k,
        "LLM_MAX_TOKENS_EXTRACTION": req.llm_max_tokens_extraction,
    }
    # Boolean values must be lowercased for Pydantic settings env parsing
    # (pydantic-settings reads "true"/"false" for bool fields)
    result: dict[str, str] = {}
    for env_key, value in mapping.items():
        if value is None:
            continue
        if isinstance(value, bool):
            result[env_key] = "true" if value else "false"
        else:
            result[env_key] = str(value)
    return result


# ── Background task ───────────────────────────────────────────────────────────

def _run_ablation_task(job_id: str, req: AblationRunRequest) -> None:
    """Execute the full ablation pipeline in a background thread."""
    set_running(job_id)
    try:
        from src.config.settings import get_settings
        from src.evaluation.ragas_runner import run_ragas_evaluation
        from src.graph.builder_graph import run_builder
        from src.ingestion.pdf_loader import load_pdf

        dataset_path = Path(req.dataset)
        if not dataset_path.is_absolute():
            dataset_path = _ROOT / dataset_path
        if not dataset_path.exists():
            raise FileNotFoundError(f"Dataset not found: {dataset_path}")

        # Derive doc/ddl paths from the fixture dir alongside gold_standard.json
        fixture_dir = dataset_path.parent
        doc_paths_raw = sorted(fixture_dir.glob("*.txt")) + sorted(fixture_dir.glob("*.md"))
        doc_paths = [str(p) for p in doc_paths_raw if p.name != "gold_standard.json"]
        ddl_paths = [str(p) for p in sorted(fixture_dir.glob("*.sql"))]

        env_overrides = _build_env_overrides(req)

        with _settings_override(env_overrides):
            result: dict[str, Any] = {}

            if not req.skip_builder:
                builder_state = run_builder(
                    raw_documents=doc_paths,
                    ddl_paths=ddl_paths,
                    production=False,
                    clear_graph=True,
                    use_lazy_extraction=req.lazy_extraction if req.lazy_extraction else None,
                    study_id=req.study_id,
                )
                result["builder"] = {
                    "triplets_extracted": len(builder_state.get("triplets", [])),
                    "entities_resolved": len(builder_state.get("entities", [])),
                    "tables_parsed": len(builder_state.get("tables", [])),
                    "tables_completed": len(builder_state.get("completed_tables", [])),
                    "parent_chunks": len(builder_state.get("parent_chunks", [])),
                    "child_chunks": len(builder_state.get("chunks", [])),
                }

            ragas_metrics = run_ragas_evaluation(
                dataset_path=dataset_path,
                run_ragas=req.run_ragas,
                ragas_model=req.ragas_model,
            )
            result["ragas_metrics"] = ragas_metrics

        set_done(job_id, result)
    except Exception as exc:  # noqa: BLE001
        set_failed(job_id, str(exc))


# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.post(
    "/run",
    response_model=AblationJobResponse,
    summary="Launch a custom ablation run",
    description=(
        "Start an ablation run with any combination of feature flags and hyperparameters. "
        "Returns a `job_id` to poll for status and results."
    ),
)
def post_ablation_run(
    req: AblationRunRequest,
    background_tasks: BackgroundTasks,
) -> AblationJobResponse:
    job_id = create_job(meta={"study_id": req.study_id, "dataset": req.dataset})
    background_tasks.add_task(_run_ablation_task, job_id, req)
    return AblationJobResponse(
        job_id=job_id,
        status="queued",
        study_id=req.study_id,
        dataset=req.dataset,
    )


@router.get(
    "/status/{job_id}",
    response_model=AblationResultResponse,
    summary="Poll ablation job status and results",
    description="Returns the current state of an ablation job. When `status='done'`, includes `summary` and optional `ragas` metrics.",
)
def get_ablation_status(job_id: str) -> AblationResultResponse:
    job = get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail=f"Job '{job_id}' not found.")

    result = job.get("result") or {}
    ragas_metrics = result.get("ragas_metrics", {})
    builder_info = result.get("builder", {})

    # Compute a simple summary from ragas_metrics if available
    summary: dict[str, Any] | None = None
    if ragas_metrics:
        summary = {
            "triplets_extracted": builder_info.get("triplets_extracted"),
            "entities_resolved": builder_info.get("entities_resolved"),
            "tables_parsed": builder_info.get("tables_parsed"),
            "tables_completed": builder_info.get("tables_completed"),
        }

    # Separate RAGAS float metrics from the rest
    ragas: dict[str, float] | None = None
    ragas_keys = {"faithfulness", "answer_relevancy", "context_precision", "context_recall"}
    ragas_values = {k: v for k, v in ragas_metrics.items() if k in ragas_keys and isinstance(v, (int, float))}
    if ragas_values:
        ragas = ragas_values

    return AblationResultResponse(
        job_id=job_id,
        status=job["status"],
        study_id=job["meta"].get("study_id", ""),
        error=job.get("error"),
        summary=summary,
        ragas=ragas,
    )


@router.get(
    "/jobs",
    response_model=list[AblationJobResponse],
    summary="List all ablation jobs",
    description="Returns all submitted ablation jobs with their current status.",
)
def get_ablation_jobs() -> list[AblationJobResponse]:
    jobs = list_jobs()
    return [
        AblationJobResponse(
            job_id=j["job_id"],
            status=j["status"],
            study_id=j["meta"].get("study_id", ""),
            dataset=j["meta"].get("dataset", ""),
        )
        for j in jobs
    ]


@router.get(
    "/matrix",
    response_model=list[AblationMatrixEntry],
    summary="List the predefined ablation matrix (AB-00 … AB-20)",
    description=(
        "Returns all 21 pre-configured ablation conditions defined in ABLATION_MATRIX. "
        "Use study_id from this list as input to POST /ablation/run to replicate a study."
    ),
)
def get_ablation_matrix() -> list[AblationMatrixEntry]:
    return [
        AblationMatrixEntry(
            study_id=sid,
            description=cfg["description"],
            env_overrides=cfg["env_overrides"],
            run_ragas=cfg.get("run_ragas", False),
        )
        for sid, cfg in ABLATION_MATRIX.items()
    ]


@router.get(
    "/datasets",
    response_model=list[str],
    summary="List available evaluation datasets",
    description="Scans tests/fixtures/ and returns relative paths to all gold_standard.json files.",
)
def get_ablation_datasets() -> list[str]:
    fixture_dir = _fixtures_dir()
    if not fixture_dir.exists():
        return []
    paths = sorted(fixture_dir.rglob("gold_standard.json"))
    return [str(p.relative_to(_ROOT)) for p in paths]
