"""E2E Demo REST API — /api/v1/demo/..."""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Any

from fastapi import APIRouter, BackgroundTasks, File, HTTPException, UploadFile
from pydantic import Field

from src.api.jobs import create_job, get_job, list_jobs, set_done, set_failed, set_running
from src.api.models import (
    BuildRequest,
    BuildRequestWithUpload,
    BuildResultResponse,
    GraphStatsResponse,
    PipelineJobResponse,
    PipelineRequest,
    PipelineRequestWithUpload,
    PipelineResultResponse,
    QueryRequest,
    QueryResponse,
)

router = APIRouter(prefix="/demo", tags=["E2E Demo"])

_ROOT = Path(__file__).parent.parent.parent  # repo root


# ── Helpers ───────────────────────────────────────────────────────────────────


def _to_abs(path: str) -> str:
    p = Path(path)
    return str(p if p.is_absolute() else _ROOT / p)


async def _save_uploads(files: list[UploadFile]) -> list[str]:
    """Save uploaded files to temp directory and return their absolute paths."""
    temp_dir = Path(tempfile.gettempdir()) / "thesis_uploads"
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    paths = []
    for file in files:
        temp_file = temp_dir / file.filename
        content = await file.read()
        temp_file.write_bytes(content)
        paths.append(str(temp_file))
    
    return paths


def _query_result_to_response(result: dict[str, Any]) -> QueryResponse:
    contexts = result.get("retrieved_contexts", [])
    previews = [c[:300] for c in contexts[:3]]
    return QueryResponse(
        answer=result.get("final_answer", ""),
        sources=result.get("sources", []),
        retrieval_quality_score=float(result.get("retrieval_quality_score", 0.0)),
        retrieval_chunk_count=int(result.get("retrieval_chunk_count", 0)),
        gate_decision=result.get("retrieval_gate_decision", "proceed"),
        grounded=bool(result.get("grader_grounded", True)),
        context_previews=previews,
    )


def _build_state_to_response(
    job_id: str,
    status: str,
    error: str | None,
    builder: dict[str, Any] | None,
) -> BuildResultResponse:
    if builder is None:
        return BuildResultResponse(job_id=job_id, status=status, error=error)  # type: ignore[arg-type]
    return BuildResultResponse(
        job_id=job_id,
        status=status,  # type: ignore[arg-type]
        error=error,
        triplets_extracted=builder.get("triplets_extracted"),
        entities_resolved=builder.get("entities_resolved"),
        tables_parsed=builder.get("tables_parsed"),
        tables_completed=builder.get("tables_completed"),
        parent_chunks=builder.get("parent_chunks"),
        child_chunks=builder.get("child_chunks"),
    )


# ── Background tasks ──────────────────────────────────────────────────────────


def _run_build_task(job_id: str, req: BuildRequest) -> None:
    set_running(job_id)
    try:
        from src.graph.builder_graph import run_builder

        doc_paths = [_to_abs(p) for p in req.doc_paths]
        ddl_paths = [_to_abs(p) for p in req.ddl_paths]

        builder_state = run_builder(
            raw_documents=doc_paths,
            ddl_paths=ddl_paths,
            production=False,
            clear_graph=req.clear_graph,
            use_lazy_extraction=req.lazy_extraction if req.lazy_extraction else None,
            study_id=req.study_id,
        )
        result = {
            "builder": {
                "triplets_extracted": len(builder_state.get("triplets", [])),
                "entities_resolved": len(builder_state.get("entities", [])),
                "tables_parsed": len(builder_state.get("tables", [])),
                "tables_completed": len(builder_state.get("completed_tables", [])),
                "parent_chunks": len(builder_state.get("parent_chunks", [])),
                "child_chunks": len(builder_state.get("chunks", [])),
            }
        }
        set_done(job_id, result)
    except Exception as exc:  # noqa: BLE001
        set_failed(job_id, str(exc))


def _run_pipeline_task(job_id: str, req: PipelineRequest) -> None:
    set_running(job_id)
    try:
        from src.generation.query_graph import run_query
        from src.graph.builder_graph import run_builder

        doc_paths = [_to_abs(p) for p in req.doc_paths]
        ddl_paths = [_to_abs(p) for p in req.ddl_paths]

        # 1. Build the Knowledge Graph
        builder_state = run_builder(
            raw_documents=doc_paths,
            ddl_paths=ddl_paths,
            production=False,
            clear_graph=req.clear_graph,
            use_lazy_extraction=req.lazy_extraction if req.lazy_extraction else None,
            study_id=req.study_id,
        )
        builder_summary = {
            "triplets_extracted": len(builder_state.get("triplets", [])),
            "entities_resolved": len(builder_state.get("entities", [])),
            "tables_parsed": len(builder_state.get("tables", [])),
            "tables_completed": len(builder_state.get("completed_tables", [])),
            "parent_chunks": len(builder_state.get("parent_chunks", [])),
            "child_chunks": len(builder_state.get("chunks", [])),
        }

        # 2. Answer each question
        raw_answers: list[dict[str, Any]] = []
        for idx, question in enumerate(req.questions):
            qr = run_query(question, query_index=idx, study_id=req.study_id)
            raw_answers.append(qr)

        result: dict[str, Any] = {
            "builder": builder_summary,
            "answers": raw_answers,
        }

        # 3. Optionally run RAGAS (only if expected answers are resolvable)
        if req.run_ragas:
            from src.evaluation.ragas_runner import run_ragas_evaluation

            fixture_dir = Path(doc_paths[0]).parent if doc_paths else None
            ragas_path = (fixture_dir / "gold_standard.json") if fixture_dir else None
            if ragas_path and ragas_path.exists():
                ragas_metrics = run_ragas_evaluation(dataset_path=ragas_path, run_ragas=True)
                result["ragas"] = ragas_metrics

        set_done(job_id, result)
    except Exception as exc:  # noqa: BLE001
        set_failed(job_id, str(exc))


# ── Endpoints ─────────────────────────────────────────────────────────────────


@router.post(
    "/build",
    response_model=BuildResultResponse,
    summary="Start Knowledge Graph build",
    description=(
        "Ingest documentation files and DDL schemas into Neo4j. "
        "Runs triplet extraction, entity resolution, mapping, and Cypher upsert asynchronously. "
        "Returns a `job_id` — poll GET /demo/build/{job_id} for results."
    ),
)
def post_build(req: BuildRequest, background_tasks: BackgroundTasks) -> BuildResultResponse:
    job_id = create_job(meta={"type": "build", "study_id": req.study_id})
    background_tasks.add_task(_run_build_task, job_id, req)
    return BuildResultResponse(job_id=job_id, status="queued")  # type: ignore[arg-type]


@router.get(
    "/build/{job_id}",
    response_model=BuildResultResponse,
    summary="Get Knowledge Graph build status",
    description=(
        "Poll the result of a build job. `status` transitions: queued → running → done | failed."
    ),
)
def get_build_status(job_id: str) -> BuildResultResponse:
    job = get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail=f"Job '{job_id}' not found.")
    builder = (job.get("result") or {}).get("builder")
    return _build_state_to_response(job_id, job["status"], job.get("error"), builder)


@router.post(
    "/build/upload",
    response_model=BuildResultResponse,
    summary="Build KG from uploaded documentation and DDL files",
    description=(
        "Upload documentation (PDF, MD, TXT) and SQL DDL files directly. "
        "Files are saved temporarily and processed like the path-based /build endpoint. "
        "Returns `job_id` — poll GET /demo/build/{job_id} for results. "
        "Useful for AWS and cloud deployments."
    ),
)
async def post_build_upload(
    doc_files: list[UploadFile] = File(..., description="Documentation files"),
    ddl_files: list[UploadFile] = File(..., description="DDL SQL files"),
    clear_graph: bool = True,
    study_id: str = "demo",
    lazy_extraction: bool = False,
    background_tasks: BackgroundTasks,
) -> BuildResultResponse:
    """Upload files and trigger async build. Returns job_id for polling."""
    try:
        doc_paths = await _save_uploads(doc_files)
        ddl_paths = await _save_uploads(ddl_files)
        
        req = BuildRequest(
            doc_paths=doc_paths,
            ddl_paths=ddl_paths,
            clear_graph=clear_graph,
            study_id=study_id,
            lazy_extraction=lazy_extraction,
        )
        
        job_id = create_job(meta={"type": "build", "study_id": study_id})
        background_tasks.add_task(_run_build_task, job_id, req)
        return BuildResultResponse(job_id=job_id, status="queued")  # type: ignore[arg-type]
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=400, detail=f"Upload failed: {exc}") from exc


@router.post(
    "/pipeline/upload",
    response_model=PipelineJobResponse,
    summary="Run full E2E pipeline from uploaded files",
    description=(
        "Upload docs + DDL + questions, then run build + query. "
        "Returns `job_id` — poll GET /demo/pipeline/{job_id} for results. "
        "Best for AWS and production deployments."
    ),
)
async def post_pipeline_upload(
    doc_files: list[UploadFile] = File(..., description="Documentation files"),
    ddl_files: list[UploadFile] = File(..., description="DDL SQL files"),
    questions: list[str] = Field(..., description="Questions to answer (JSON array as form field)"),
    clear_graph: bool = True,
    lazy_extraction: bool = False,
    run_ragas: bool = False,
    study_id: str = "demo",
    background_tasks: BackgroundTasks,
) -> PipelineJobResponse:
    """Upload files + questions and trigger async E2E pipeline. Returns job_id for polling."""
    try:
        doc_paths = await _save_uploads(doc_files)
        ddl_paths = await _save_uploads(ddl_files)
        
        req = PipelineRequest(
            doc_paths=doc_paths,
            ddl_paths=ddl_paths,
            questions=questions,
            clear_graph=clear_graph,
            lazy_extraction=lazy_extraction,
            run_ragas=run_ragas,
            study_id=study_id,
        )
        
        job_id = create_job(
            meta={"type": "pipeline", "study_id": study_id, "num_questions": len(questions)},
        )
        background_tasks.add_task(_run_pipeline_task, job_id, req)
        return PipelineJobResponse(job_id=job_id, status="queued", num_questions=len(questions))
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=400, detail=f"Upload failed: {exc}") from exc


@router.post(
    "/query",
    response_model=QueryResponse,
    summary="Answer a question from the Knowledge Graph",
    description=(
        "Synchronous endpoint. Runs hybrid retrieval + reranking + LLM generation "
        "on the currently loaded Neo4j Knowledge Graph and returns an answer."
    ),
)
def post_query(req: QueryRequest) -> QueryResponse:
    try:
        from src.generation.query_graph import run_query

        result = run_query(req.question)
        return _query_result_to_response(result)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post(
    "/pipeline",
    response_model=PipelineJobResponse,
    summary="Run complete E2E pipeline (build + query)",
    description=(
        "Starts a full end-to-end pipeline: builds the Knowledge Graph, "
        "then answers all provided questions. "
        "Returns a `job_id` — poll GET /demo/pipeline/{job_id}."
    ),
)
def post_pipeline(req: PipelineRequest, background_tasks: BackgroundTasks) -> PipelineJobResponse:
    job_id = create_job(
        meta={"type": "pipeline", "study_id": req.study_id, "num_questions": len(req.questions)},
    )
    background_tasks.add_task(_run_pipeline_task, job_id, req)
    return PipelineJobResponse(job_id=job_id, status="queued", num_questions=len(req.questions))


@router.get(
    "/pipeline/{job_id}",
    response_model=PipelineResultResponse,
    summary="Get E2E pipeline status and results",
    description=(
        "Poll a pipeline job. When `status='done'`, "
        "includes builder metrics and per-question answers."
    ),
)
def get_pipeline_status(job_id: str) -> PipelineResultResponse:
    job = get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail=f"Job '{job_id}' not found.")

    result = job.get("result") or {}
    error = job.get("error")
    status = job["status"]

    builder_data = result.get("builder")
    build_response: BuildResultResponse | None = None
    if builder_data is not None:
        build_response = _build_state_to_response(job_id, status, error, builder_data)

    raw_answers = result.get("answers", [])
    answers: list[QueryResponse] | None = None
    if raw_answers:
        answers = [_query_result_to_response(a) for a in raw_answers]

    ragas = result.get("ragas")

    return PipelineResultResponse(
        job_id=job_id,
        status=status,  # type: ignore[arg-type]
        error=error,
        builder=build_response,
        answers=answers,
        ragas=ragas,
    )


@router.get(
    "/jobs",
    response_model=list[PipelineJobResponse],
    summary="List all demo jobs (build + pipeline)",
    description="Returns all submitted demo jobs.",
)
def get_demo_jobs() -> list[PipelineJobResponse]:
    jobs = [j for j in list_jobs() if j["meta"].get("type") in {"build", "pipeline"}]
    return [
        PipelineJobResponse(
            job_id=j["job_id"],
            status=j["status"],  # type: ignore[arg-type]
            num_questions=j["meta"].get("num_questions", 0),
        )
        for j in jobs
    ]


@router.get(
    "/graph/stats",
    response_model=GraphStatsResponse,
    summary="Get current Knowledge Graph statistics",
    description=(
        "Synchronous. Queries Neo4j for node and relationship counts "
        "across all label types: BusinessConcept, PhysicalTable, ParentChunk, Chunk."
    ),
)
def get_graph_stats() -> GraphStatsResponse:
    try:
        from src.graph.neo4j_client import Neo4jClient

        cypher_nodes = """
        RETURN
          sum(CASE WHEN 'BusinessConcept' IN labels(n) THEN 1 ELSE 0 END) AS business_concepts,
          sum(CASE WHEN 'PhysicalTable'   IN labels(n) THEN 1 ELSE 0 END) AS physical_tables,
          sum(CASE WHEN 'ParentChunk'     IN labels(n) THEN 1 ELSE 0 END) AS parent_chunks,
          sum(CASE WHEN 'Chunk'           IN labels(n) THEN 1 ELSE 0 END) AS child_chunks
        """
        counts_query = "MATCH (n) " + cypher_nodes
        rel_query = "MATCH ()-[r]->() RETURN count(r) AS total_relationships"
        rel_mentions = "MATCH ()-[r:MENTIONS]->() RETURN count(r) AS n"
        rel_maps = "MATCH ()-[r:MAPPED_TO]->() RETURN count(r) AS n"
        node_total = "MATCH (n) RETURN count(n) AS total_nodes"

        with Neo4jClient() as client:
            row = client.execute_cypher(counts_query)[0]
            total_nodes = client.execute_cypher(node_total)[0]["total_nodes"]
            total_rels = client.execute_cypher(rel_query)[0]["total_relationships"]
            mentions = client.execute_cypher(rel_mentions)[0]["n"]
            maps_to = client.execute_cypher(rel_maps)[0]["n"]

        return GraphStatsResponse(
            business_concepts=int(row.get("business_concepts", 0) or 0),
            physical_tables=int(row.get("physical_tables", 0) or 0),
            parent_chunks=int(row.get("parent_chunks", 0) or 0),
            child_chunks=int(row.get("child_chunks", 0) or 0),
            mentions_edges=int(mentions or 0),
            maps_to_edges=int(maps_to or 0),
            total_nodes=int(total_nodes or 0),
            total_relationships=int(total_rels or 0),
        )
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=503, detail=f"Neo4j unavailable: {exc}") from exc
