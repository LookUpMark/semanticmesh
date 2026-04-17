"""Ablation Studies REST API — /api/v1/ablation/..."""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

from fastapi import APIRouter, BackgroundTasks, HTTPException
from fastapi.responses import JSONResponse

from src.api.jobs import create_job, get_job, list_jobs, set_done, set_failed, set_running
from src.api.models import (
    AblationJobResponse,
    AblationMatrixEntry,
    AblationResultResponse,
    AblationRunRequest,
    CustomAblationRequest,
    PresetAblationJobResponse,
    PresetAblationRequest,
)
from src.evaluation.ablation_runner import ABLATION_MATRIX, _settings_override
from src.utils.text_utils import normalize_source_name as _normalize_source

router = APIRouter(prefix="/ablation", tags=["Ablation Studies"])

# ── Helpers ───────────────────────────────────────────────────────────────────

_ROOT = Path(__file__).parent.parent.parent  # repo root


def _fixtures_dir() -> Path:
    return _ROOT / "tests" / "fixtures"


def _build_env_overrides(req: AblationRunRequest) -> dict[str, str]:
    """Translate non-None hyperparameter and LLM fields in the request to env vars."""
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
        # LLM model overrides — forwarded as env vars read by settings
        "LLM_MODEL_REASONING": getattr(req, "reasoning_model", None),
        "LLM_MODEL_EXTRACTION": getattr(req, "extraction_model", None),
        "PROVIDER_BASE_URL": getattr(req, "provider_base_url", None),
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
    """Execute the full ablation pipeline in a background thread.

    Stages: (1) Builder Graph → (2) Query Evaluation → (3) optional RAGAS → (4) Bundle
    """
    set_running(job_id)
    try:
        from src.config.settings import get_settings
        from src.generation.query_graph import run_query
        from src.graph.builder_graph import run_builder

        dataset_path = Path(req.dataset)
        if not dataset_path.is_absolute():
            dataset_path = _ROOT / dataset_path
        if not dataset_path.exists():
            raise FileNotFoundError(f"Dataset not found: {dataset_path}")

        # Load QA pairs from gold_standard.json
        dataset_raw = json.loads(dataset_path.read_text(encoding="utf-8"))
        all_pairs = (
            dataset_raw.get("pairs")
            or dataset_raw.get("qa_pairs")
            or dataset_raw.get("questions")
            or []
        )
        dataset_id = dataset_raw.get("dataset_id", dataset_path.parent.name)
        if req.max_samples is not None and req.max_samples > 0:
            all_pairs = all_pairs[: req.max_samples]

        # Derive doc/ddl paths from the fixture dir alongside gold_standard.json
        fixture_dir = dataset_path.parent
        doc_paths_raw = sorted(fixture_dir.glob("*.txt")) + sorted(fixture_dir.glob("*.md"))
        doc_paths = [str(p) for p in doc_paths_raw if p.name != "gold_standard.json"]
        ddl_paths = [str(p) for p in sorted(fixture_dir.glob("*.sql"))]

        env_overrides = _build_env_overrides(req)

        with _settings_override(env_overrides):
            settings = get_settings()
            result: dict[str, Any] = {
                "config": {
                    "extraction_model": settings.llm_model_extraction,
                    "reasoning_model": settings.llm_model_reasoning,
                    "retrieval_mode": settings.retrieval_mode,
                    "enable_reranker": settings.enable_reranker,
                    "chunk_size": settings.chunk_size,
                    "chunk_overlap": settings.chunk_overlap,
                    "er_similarity_threshold": settings.er_similarity_threshold,
                },
            }

            # ── Stage 1: Builder Graph ────────────────────────────────────
            builder_info: dict[str, Any] = {}
            if not req.skip_builder:
                t0 = time.time()
                builder_state = run_builder(
                    raw_documents=doc_paths,
                    ddl_paths=ddl_paths,
                    production=False,
                    clear_graph=True,
                    use_lazy_extraction=req.lazy_extraction if req.lazy_extraction else None,
                    trace_enabled=True,
                    study_id=req.study_id,
                )
                builder_elapsed = time.time() - t0

                triplets = builder_state.get("triplets", [])
                entities = builder_state.get("entities", [])
                tables = builder_state.get("tables", [])
                completed = builder_state.get("completed_tables", [])

                parent_chunks_raw = builder_state.get("parent_chunks") or []
                chunks_raw = builder_state.get("chunks") or []

                n_parent = len(parent_chunks_raw) if isinstance(parent_chunks_raw, list) else 0

                builder_info = {
                    "triplets_extracted": len(triplets),
                    "entities_resolved": len(entities),
                    "tables_parsed": len(tables),
                    "tables_completed": len(completed),
                    "cypher_failed": bool(builder_state.get("cypher_failed", False)),
                    "failed_mappings": list(builder_state.get("failed_mappings", [])),
                    "ingestion_errors": list(builder_state.get("ingestion_errors", [])),
                    "parent_chunks": n_parent,
                    "child_chunks": len(chunks_raw),
                    "elapsed_s": round(builder_elapsed, 1),
                }
                result["builder"] = builder_info

            # ── Stage 2: Query Evaluation ─────────────────────────────────
            per_question: list[dict[str, Any]] = []
            grounded_count = 0
            abstained_count = 0
            t1 = time.time()

            for i, pair in enumerate(all_pairs):
                question = pair.get("question", "")
                expected_answer = pair.get("expected_answer", pair.get("answer", ""))
                expected_sources = pair.get("expected_sources", [])

                qr = run_query(
                    user_query=question,
                    trace_enabled=True,
                    query_index=i,
                    study_id=req.study_id,
                )

                answer = qr.get("final_answer", "")
                sources = list(qr.get("sources", []))
                gate = qr.get("retrieval_gate_decision", "proceed")
                top_score = qr.get("retrieval_quality_score", 0.0)
                chunk_count = qr.get("retrieval_chunk_count", 0)
                grader_grounded = qr.get("grader_grounded", True)
                grounded = bool(grader_grounded and gate != "abstain_early")

                if grounded:
                    grounded_count += 1
                if gate == "abstain_early":
                    abstained_count += 1

                # GT source coverage
                covered = [
                    s
                    for s in expected_sources
                    if any(_normalize_source(s) in _normalize_source(src) for src in sources)
                ]
                gt_coverage = len(covered) / len(expected_sources) if expected_sources else 1.0

                per_question.append(
                    {
                        "query_id": pair.get("query_id", f"Q{i + 1:03d}"),
                        "question": question,
                        "query_type": pair.get("query_type", ""),
                        "difficulty": pair.get("difficulty", ""),
                        "expected_answer": expected_answer,
                        "expected_sources": expected_sources,
                        "generated_answer": answer,
                        "sources_retrieved": sources,
                        "contexts_retrieved": [c[:500] for c in qr.get("retrieved_contexts", [])],
                        "covered_sources": covered,
                        "gt_coverage": gt_coverage,
                        "grounded": grounded,
                        "gate_decision": gate,
                        "retrieval_quality_score": top_score,
                        "chunk_count": chunk_count,
                        "grader_rejection_count": qr.get("grader_rejection_count", 0),
                        "grader_consistency_valid": qr.get("grader_consistency_valid", True),
                        "context_sufficiency": qr.get("context_sufficiency", ""),
                    }
                )

            query_elapsed = time.time() - t1
            total_q = len(per_question)
            avg_gt = sum(pq["gt_coverage"] for pq in per_question) / total_q if total_q else 0.0
            avg_score = (
                sum(pq["retrieval_quality_score"] for pq in per_question) / total_q
                if total_q
                else 0.0
            )
            avg_chunks = sum(pq["chunk_count"] for pq in per_question) / total_q if total_q else 0.0

            result["query"] = {
                "total_questions": total_q,
                "grounded_count": grounded_count,
                "grounded_rate": grounded_count / total_q if total_q else 0.0,
                "abstained_count": abstained_count,
                "avg_gt_coverage": avg_gt,
                "avg_top_score": avg_score,
                "avg_chunk_count": avg_chunks,
                "elapsed_s": round(query_elapsed, 1),
            }
            result["per_question"] = per_question

            # ── Stage 3: RAGAS Evaluation (optional) ──────────────────────
            ragas_metrics: dict[str, Any] = {}
            if req.run_ragas:
                from src.evaluation.ragas_runner import run_ragas_evaluation

                ragas_metrics = run_ragas_evaluation(
                    dataset_path=dataset_path,
                    run_ragas=True,
                    evaluator_model=req.ragas_model,
                    max_samples=req.max_samples,
                )
            result["ragas_metrics"] = ragas_metrics

            # ── Stage 4: Evaluation Bundle ────────────────────────────────
            from src.evaluation.bundle_writer import write_evaluation_bundle

            bundle_dir = (
                _ROOT / "outputs" / "ablation" / req.study_id / "datasets" / dataset_id
            )
            bundle_dir.mkdir(parents=True, exist_ok=True)
            bundle_path = write_evaluation_bundle(
                output_dir=bundle_dir,
                study_id=req.study_id,
                dataset_id=dataset_id,
                dataset_info=dataset_raw,
                config=result.get("config", {}),
                builder_info=builder_info,
                query_summary=result.get("query", {}),
                per_question=per_question,
                ragas_metrics=ragas_metrics,
            )
            result["bundle_path"] = str(bundle_path)

        set_done(job_id, result)
    except Exception as exc:  # noqa: BLE001
        set_failed(job_id, str(exc))


def _run_preset_ablation_task(
    job_id: str,
    req: CustomAblationRequest,
    preset_env: dict[str, str],
) -> None:
    """Wrapper that merges preset matrix env vars before running the ablation task.

    The matrix env overrides (feature flags etc.) are injected first, then the
    request-level LLM overrides (reasoning_model, extraction_model) are applied
    on top via _build_env_overrides — so user-supplied LLM overrides always win.
    """
    # Patch the request's env overrides into os.environ temporarily
    # by preloading the merged dict into LMSTUDIO_BASE_URL / LLM_MODEL_*
    # The cleanest approach: temporarily set env vars inside _settings_override,
    # which _run_ablation_task will then pick up via _build_env_overrides.
    # We store the preset env in req's __dict__ as _preset_env to be merged.
    req.__dict__["_preset_env"] = preset_env
    _run_ablation_task_with_preset(job_id, req, preset_env)


def _run_ablation_task_with_preset(
    job_id: str,
    req: CustomAblationRequest,
    preset_env: dict[str, str],
) -> None:
    """Like _run_ablation_task but uses preset_env as the base env override dict."""
    set_running(job_id)
    try:
        from src.config.settings import get_settings
        from src.generation.query_graph import run_query
        from src.graph.builder_graph import run_builder

        dataset_path = Path(req.dataset)
        if not dataset_path.is_absolute():
            dataset_path = _ROOT / dataset_path
        if not dataset_path.exists():
            raise FileNotFoundError(f"Dataset not found: {dataset_path}")

        dataset_raw = json.loads(dataset_path.read_text(encoding="utf-8"))
        all_pairs = (
            dataset_raw.get("pairs")
            or dataset_raw.get("qa_pairs")
            or dataset_raw.get("questions")
            or []
        )
        dataset_id = dataset_raw.get("dataset_id", dataset_path.parent.name)
        if req.max_samples is not None and req.max_samples > 0:
            all_pairs = all_pairs[: req.max_samples]

        fixture_dir = dataset_path.parent
        doc_paths_raw = sorted(fixture_dir.glob("*.txt")) + sorted(fixture_dir.glob("*.md"))
        doc_paths = [str(p) for p in doc_paths_raw if p.name != "gold_standard.json"]
        ddl_paths = [str(p) for p in sorted(fixture_dir.glob("*.sql"))]

        # Merge: preset matrix overrides first, then request-level LLM overrides
        req_llm_env = _build_env_overrides(req)
        env_overrides = {**preset_env, **req_llm_env}

        with _settings_override(env_overrides):
            settings = get_settings()
            result: dict[str, Any] = {
                "config": {
                    "extraction_model": settings.llm_model_extraction,
                    "reasoning_model": settings.llm_model_reasoning,
                    "retrieval_mode": settings.retrieval_mode,
                    "enable_reranker": settings.enable_reranker,
                    "chunk_size": settings.chunk_size,
                    "chunk_overlap": settings.chunk_overlap,
                    "er_similarity_threshold": settings.er_similarity_threshold,
                },
            }

            # ── Stage 1: Builder Graph ─────────────────────────────────────
            builder_state: Any = {}
            builder_info: dict[str, Any] = {}
            if not req.skip_builder:
                t0 = time.time()
                builder_state = run_builder(
                    raw_documents=doc_paths,
                    ddl_paths=ddl_paths,
                    production=False,
                    clear_graph=True,
                    study_id=req.study_id,
                )
                elapsed = time.time() - t0
                builder_info = {
                    "triplets_extracted": len(builder_state.get("triplets") or []),
                    "entities_resolved": len(builder_state.get("resolved_entities") or []),
                    "tables_parsed": len(builder_state.get("table_schemas") or []),
                    "tables_completed": len(builder_state.get("completed_tables") or []),
                    "cypher_failed": builder_state.get("cypher_failed", False),
                    "elapsed_s": round(elapsed, 1),
                }
            result["builder"] = builder_info

            # ── Stage 2: Query Evaluation ──────────────────────────────────
            per_question: list[dict[str, Any]] = []
            t1 = time.time()
            for item in all_pairs:
                question = item.get("question", "")
                expected = item.get("answer", item.get("expected_answer", ""))
                metadata = item.get("metadata", {})
                try:
                    query_state = run_query(user_query=question)
                    answer = query_state.get("answer", "")
                    contexts = query_state.get("contexts") or []
                    score = (
                        query_state.get("rerank_scores", [0.0])[0]
                        if query_state.get("rerank_scores")
                        else 0.0
                    )
                    is_grounded = bool(query_state.get("is_grounded", True))
                    abstained = "cannot" in answer.lower() or "don't have" in answer.lower()
                    exp_lower = expected.lower()
                    ans_lower = answer.lower()
                    stopwords = {"the", "a", "an", "is", "are", "in", "of", "for", "to"}
                    exp_words = set(exp_lower.split()) - stopwords
                    gt_coverage = (
                        sum(1 for w in exp_words if w in ans_lower) / len(exp_words)
                        if exp_words
                        else 0.0
                    )
                    per_question.append(
                        {
                            "question": question,
                            "expected": expected,
                            "answer": answer,
                            "is_grounded": is_grounded,
                            "abstained": abstained,
                            "gt_coverage": round(gt_coverage, 3),
                            "top_rerank_score": round(score, 4),
                            "chunk_count": len(contexts),
                            "metadata": metadata,
                        }
                    )
                except Exception as q_exc:  # noqa: BLE001
                    per_question.append(
                        {
                            "question": question,
                            "expected": expected,
                            "answer": "",
                            "error": str(q_exc),
                            "is_grounded": False,
                            "abstained": False,
                            "gt_coverage": 0.0,
                            "top_rerank_score": 0.0,
                            "chunk_count": 0,
                            "metadata": metadata,
                        }
                    )
            query_elapsed = time.time() - t1
            total_q = len(per_question)
            grounded_count = sum(1 for pq in per_question if pq.get("is_grounded"))
            abstained_count = sum(1 for pq in per_question if pq.get("abstained"))
            avg_gt = sum(pq["gt_coverage"] for pq in per_question) / total_q if total_q else 0.0
            avg_score = (
                sum(pq["top_rerank_score"] for pq in per_question) / total_q if total_q else 0.0
            )
            avg_chunks = sum(pq["chunk_count"] for pq in per_question) / total_q if total_q else 0.0
            result["query"] = {
                "total_questions": total_q,
                "grounded_count": grounded_count,
                "grounded_rate": grounded_count / total_q if total_q else 0.0,
                "abstained_count": abstained_count,
                "avg_gt_coverage": avg_gt,
                "avg_top_score": avg_score,
                "avg_chunk_count": avg_chunks,
                "elapsed_s": round(query_elapsed, 1),
            }
            result["per_question"] = per_question

            ragas_metrics: dict[str, Any] = {}
            if req.run_ragas:
                from src.evaluation.ragas_runner import run_ragas_evaluation

                ragas_metrics = run_ragas_evaluation(
                    dataset_path=dataset_path,
                    run_ragas=True,
                    evaluator_model=req.ragas_model,
                    max_samples=req.max_samples,
                )
            result["ragas_metrics"] = ragas_metrics

            from src.evaluation.bundle_writer import write_evaluation_bundle

            bundle_dir = (
                _ROOT / "outputs" / "ablation" / req.study_id / "datasets" / dataset_id
            )
            bundle_dir.mkdir(parents=True, exist_ok=True)
            bundle_path = write_evaluation_bundle(
                output_dir=bundle_dir,
                study_id=req.study_id,
                dataset_id=dataset_id,
                dataset_info=dataset_raw,
                config=result.get("config", {}),
                builder_info=builder_info,
                query_summary=result.get("query", {}),
                per_question=per_question,
                ragas_metrics=ragas_metrics,
            )
            result["bundle_path"] = str(bundle_path)

        set_done(job_id, result)
    except Exception as exc:  # noqa: BLE001
        set_failed(job_id, str(exc))


# ── Endpoints ─────────────────────────────────────────────────────────────────


@router.get(
    "/matrix",
    response_model=list[AblationMatrixEntry],
    summary="Browse predefined ablation conditions (AB-00 … AB-20)",
    description=(
        "Returns all pre-configured ablation studies defined in the ablation matrix. "
        "Use the `study_id` from this list as input to **POST /ablation/run/preset**."
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
    description=(
        "Scans `tests/fixtures/` and returns relative paths to all `gold_standard.json` files. "
        "Use the returned paths as the `dataset` field in run requests."
    ),
)
def get_ablation_datasets() -> list[str]:
    fixture_dir = _fixtures_dir()
    if not fixture_dir.exists():
        return []
    paths = sorted(fixture_dir.rglob("gold_standard.json"))
    return [str(p.relative_to(_ROOT)) for p in paths]


@router.post(
    "/run/preset",
    response_model=PresetAblationJobResponse,
    summary="Launch a predefined AB-XX ablation study",
    description=(
        "Starts an ablation run using the configuration defined in the ablation matrix "
        "for the given `study_id`. All feature flags and hyperparameters are set automatically. "
        "Optionally override the LLM via `reasoning_model`, `extraction_model`, `provider_base_url` — "
        "these win over the matrix defaults. "
        "Returns a `job_id` — poll **GET /ablation/status/{job_id}** for results."
    ),
)
def post_ablation_run_preset(
    req: PresetAblationRequest,
    background_tasks: BackgroundTasks,
) -> PresetAblationJobResponse:
    if req.study_id not in ABLATION_MATRIX:
        raise HTTPException(
            status_code=422,
            detail=(
                f"Unknown study_id '{req.study_id}'. "
                f"Valid values: {sorted(ABLATION_MATRIX.keys())}. "
                "Use GET /ablation/matrix to browse all studies."
            ),
        )
    matrix_cfg = ABLATION_MATRIX[req.study_id]
    # Matrix env_overrides provide the base; LLM overrides are layered on top
    matrix_env: dict[str, str] = dict(matrix_cfg["env_overrides"])
    llm_overrides: dict[str, str] = {}
    if req.reasoning_model:
        llm_overrides["LLM_MODEL_REASONING"] = req.reasoning_model
    if req.extraction_model:
        llm_overrides["LLM_MODEL_EXTRACTION"] = req.extraction_model
    if req.provider_base_url:
        llm_overrides["PROVIDER_BASE_URL"] = req.provider_base_url
    applied_env = {**matrix_env, **llm_overrides}

    # Build an equivalent CustomAblationRequest to reuse _run_ablation_task
    custom_req = CustomAblationRequest(
        dataset=req.dataset,
        study_id=req.study_id,
        max_samples=req.max_samples,
        run_ragas=req.run_ragas,
        ragas_model=req.ragas_model,
        skip_builder=req.skip_builder,
        reasoning_model=req.reasoning_model,
        extraction_model=req.extraction_model,
        provider_base_url=req.provider_base_url,
    )
    # Inject matrix env overrides — patch the request so _build_env_overrides picks them up
    # via _settings_override inside _run_ablation_task. We store them in a side-channel
    # by temporarily setting env vars; instead we pass a pre-built override dict via
    # a wrapper task so the matrix flags are applied upstream.
    job_id = create_job(
        meta={
            "study_id": req.study_id,
            "dataset": req.dataset,
            "preset": True,
            "applied_env_overrides": applied_env,
        }
    )
    background_tasks.add_task(_run_preset_ablation_task, job_id, custom_req, applied_env)
    return PresetAblationJobResponse(
        job_id=job_id,
        status="queued",
        study_id=req.study_id,
        dataset=req.dataset,
        description=matrix_cfg["description"],
        applied_env_overrides=applied_env,
    )


@router.post(
    "/run/custom",
    response_model=AblationJobResponse,
    summary="Launch a fully custom ablation run",
    description=(
        "Start an ablation run with any combination of feature flags, hyperparameters, "
        "and LLM model overrides. All fields are optional — `None` means use the current "
        "environment/settings default. "
        "Use `reasoning_model` / `extraction_model` to override the LLM "
        "(provider is auto-detected from the model name prefix). "
        "Returns a `job_id` — poll **GET /ablation/status/{job_id}** for results."
    ),
)
def post_ablation_run_custom(
    req: CustomAblationRequest,
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


@router.post(
    "/run",
    response_model=AblationJobResponse,
    summary="Launch a custom ablation run (alias)",
    description="Alias for `POST /ablation/run/custom` — kept for backward compatibility.",
    include_in_schema=False,
)
def post_ablation_run(
    req: AblationRunRequest,
    background_tasks: BackgroundTasks,
) -> AblationJobResponse:
    return post_ablation_run_custom(req, background_tasks)


@router.get(
    "/status/{job_id}",
    response_model=AblationResultResponse,
    summary="Poll ablation job status and results",
    description=(
        "Returns the current state of an ablation job. "
        "When `status='done'`, includes `summary` and optional `ragas` metrics."
    ),
)
def get_ablation_status(job_id: str) -> AblationResultResponse:
    job = get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail=f"Job '{job_id}' not found.")

    result = job.get("result") or {}
    builder_info = result.get("builder", {})
    query_info = result.get("query", {})
    ragas_raw = result.get("ragas_metrics", {})

    # Builder + Query summary — always present when done
    summary: dict[str, Any] | None = None
    if builder_info or query_info:
        summary = {
            "triplets_extracted": builder_info.get("triplets_extracted"),
            "entities_resolved": builder_info.get("entities_resolved"),
            "tables_parsed": builder_info.get("tables_parsed"),
            "tables_completed": builder_info.get("tables_completed"),
            "cypher_failed": builder_info.get("cypher_failed"),
            "total_questions": query_info.get("total_questions"),
            "grounded_count": query_info.get("grounded_count"),
            "grounded_rate": query_info.get("grounded_rate"),
            "abstained_count": query_info.get("abstained_count"),
            "avg_gt_coverage": query_info.get("avg_gt_coverage"),
            "avg_top_score": query_info.get("avg_top_score"),
        }

    # Separate RAGAS float metrics
    ragas: dict[str, float] | None = None
    ragas_keys = {"faithfulness", "answer_relevancy", "context_precision", "context_recall"}
    ragas_values = {
        k: v for k, v in ragas_raw.items() if k in ragas_keys and isinstance(v, (int, float))
    }
    if ragas_values:
        ragas = ragas_values

    per_question = result.get("per_question")
    bundle_path = result.get("bundle_path")

    return AblationResultResponse(
        job_id=job_id,
        status=job["status"],
        study_id=job["meta"].get("study_id", ""),
        error=job.get("error"),
        summary=summary,
        ragas=ragas,
        per_question=per_question,
        bundle_path=bundle_path,
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


# ── Evaluation Bundle Endpoints ───────────────────────────────────────────────


def _bundle_path(study_id: str, dataset_id: str) -> Path:
    return (
        _ROOT
        / "notebooks"
        / "ablation"
        / "outputs" / "ablation"
        / study_id
        / dataset_id
        / "evaluation_bundle.json"
    )


@router.get(
    "/bundle/{study_id}/{dataset_id}",
    summary="Download evaluation bundle",
    description=(
        "Returns the `evaluation_bundle.json` for a completed ablation run. "
        "Contains all per-question results, builder metrics, and RAGAS scores."
    ),
)
def get_evaluation_bundle(study_id: str, dataset_id: str) -> JSONResponse:
    path = _bundle_path(study_id, dataset_id)
    if not path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Bundle not found: {study_id}/{dataset_id}. Run an ablation first.",
        )
    data = json.loads(path.read_text(encoding="utf-8"))
    return JSONResponse(content=data)


@router.get(
    "/evaluate/{study_id}/{dataset_id}",
    summary="AI-as-Judge evaluation payload",
    description=(
        "Returns the AI Judge system prompt combined with the evaluation bundle — "
        "ready to feed to any AI (Claude, GPT, etc.) for a structured qualitative evaluation. "
        "Use the returned `system_prompt` as the system message and `evaluation_bundle` as the user message."
    ),
)
def get_ai_judge_payload(study_id: str, dataset_id: str) -> JSONResponse:
    bundle_file = _bundle_path(study_id, dataset_id)
    if not bundle_file.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Bundle not found: {study_id}/{dataset_id}. Run an ablation first.",
        )

    prompt_file = _ROOT / "docs" / "AI_JUDGE_PROMPT.md"
    if not prompt_file.exists():
        raise HTTPException(
            status_code=500,
            detail="AI_JUDGE_PROMPT.md not found in docs/.",
        )


    prompt_text = prompt_file.read_text(encoding="utf-8")
    bundle_data = json.loads(bundle_file.read_text(encoding="utf-8"))

    return JSONResponse(
        content={
            "system_prompt": prompt_text,
            "evaluation_bundle": bundle_data,
            "instructions": (
                "Feed system_prompt as the system message and evaluation_bundle as the user message "
                "to any AI (Claude, GPT, etc.) to obtain a structured qualitative evaluation."
            ),
        }
    )
