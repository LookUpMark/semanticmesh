"""E2E Demo REST API — /api/v1/demo/..."""

from __future__ import annotations

import asyncio
import re
import tempfile
import threading
from pathlib import Path
from typing import Any

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from src.api.jobs import create_job, get_job, list_jobs, set_done, set_failed, set_running
from src.api.models import (
    BuildRequest,
    BuildResultResponse,
    ConversationDetail,
    ConversationMeta,
    GraphStatsResponse,
    KGSnapshotMeta,
    PipelineJobResponse,
    PipelineRequest,
    PipelineResultResponse,
    QueryRequest,
    QueryResponse,
    RenameConversationRequest,
    RenameSnapshotRequest,
    SaveConversationRequest,
    SaveSnapshotRequest,
)
from src.evaluation.ablation_runner import _settings_override as _settings_override

router = APIRouter(prefix="/demo", tags=["E2E Demo"])

_ROOT = Path(__file__).parent.parent.parent  # repo root


# ── Helpers ───────────────────────────────────────────────────────────────────


def _to_abs(path: str) -> str:
    p = Path(path).resolve()
    if not str(p).startswith(str(_ROOT.resolve())):
        raise ValueError(f"Path '{path}' is outside the allowed directory.")
    return str(p)


_MAX_UPLOAD_BYTES = 100 * 1024 * 1024  # 100 MB per file
_ALLOWED_EXTENSIONS = {".pdf", ".txt", ".md", ".sql", ".ddl"}


def _sanitize_filename(raw: str | None) -> str:
    """Strip path components and reject dangerous characters."""
    basename = Path(raw or "upload").name
    # Keep only alphanumerics, dots, dashes, underscores
    safe = re.sub(r"[^\w.\-]", "_", basename)
    return safe or "upload"


async def _save_uploads(files: list[UploadFile]) -> list[str]:
    """Save uploaded files to temp directory and return their absolute paths.

    Enforces:
    - Filename sanitisation (no path traversal)
    - 100 MB per-file size limit
    - Allowed extension whitelist
    """
    temp_dir = Path(tempfile.gettempdir()) / "thesis_uploads"
    temp_dir.mkdir(parents=True, exist_ok=True)

    paths = []
    for file in files:
        content = await file.read()

        if len(content) > _MAX_UPLOAD_BYTES:
            raise HTTPException(
                status_code=413,
                detail=f"File '{file.filename}' exceeds 100 MB limit.",
            )

        safe_name = _sanitize_filename(file.filename)
        ext = Path(safe_name).suffix.lower()
        if ext not in _ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=415,
                detail=f"Unsupported file type '{ext}'. Allowed: {sorted(_ALLOWED_EXTENSIONS)}",
            )

        temp_file = temp_dir / safe_name
        await asyncio.to_thread(temp_file.write_bytes, content)
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
    current_step: str | None = None,
) -> BuildResultResponse:
    if builder is None:
        return BuildResultResponse(job_id=job_id, status=status, error=error, current_step=current_step)  # type: ignore[arg-type]
    return BuildResultResponse(
        job_id=job_id,
        status=status,  # type: ignore[arg-type]
        error=error,
        current_step=current_step,
        triplets_extracted=builder.get("triplets_extracted"),
        entities_resolved=builder.get("entities_resolved"),
        tables_parsed=builder.get("tables_parsed"),
        tables_completed=builder.get("tables_completed"),
        parent_chunks=builder.get("parent_chunks"),
        child_chunks=builder.get("child_chunks"),
        skipped_files=builder.get("skipped_files") or None,
    )


# ── Background tasks ──────────────────────────────────────────────────────────


def _run_build_task(job_id: str, req: BuildRequest) -> None:
    set_running(job_id)
    try:
        from src.graph.builder_graph import run_builder

        doc_paths = [_to_abs(p) for p in req.doc_paths]
        ddl_paths = [_to_abs(p) for p in req.ddl_paths]

        env_overrides = req.config.to_env_overrides() if req.config else {}
        with _settings_override(env_overrides):
            builder_state = run_builder(
                raw_documents=doc_paths,
                ddl_paths=ddl_paths,
                production=False,
                clear_graph=req.clear_graph,
                force_rebuild=req.force_rebuild,
                use_lazy_extraction=req.lazy_extraction if req.lazy_extraction else None,
                study_id=req.study_id,
                job_id=job_id,  # passed through so run_builder can call set_step()
            )
        result = {
            "builder": {
                "triplets_extracted": len(builder_state.get("triplets", [])),
                "entities_resolved": len(builder_state.get("entities", [])),
                "tables_parsed": len(builder_state.get("tables", [])),
                "tables_completed": len(builder_state.get("completed_tables", [])),
                "parent_chunks": len(builder_state.get("parent_chunks", [])),
                "child_chunks": len(builder_state.get("chunks", [])),
                "skipped_files": builder_state.get("skipped_files", []),
            }
        }
        set_done(job_id, result)
    except Exception as exc:  # noqa: BLE001
        error_summary = f"{type(exc).__name__}: {str(exc)[:300]}"
        set_failed(job_id, error_summary)


def _run_pipeline_task(job_id: str, req: PipelineRequest) -> None:
    set_running(job_id)
    try:
        from src.generation.query_graph import run_query
        from src.graph.builder_graph import run_builder

        doc_paths = [_to_abs(p) for p in req.doc_paths]
        ddl_paths = [_to_abs(p) for p in req.ddl_paths]

        env_overrides = req.config.to_env_overrides() if req.config else {}
        with _settings_override(env_overrides):
            # 1. Build the Knowledge Graph
            builder_state = run_builder(
                raw_documents=doc_paths,
                ddl_paths=ddl_paths,
                production=False,
                clear_graph=req.clear_graph,
                force_rebuild=getattr(req, "force_rebuild", False),
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
                "skipped_files": builder_state.get("skipped_files", []),
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
        error_summary = f"{type(exc).__name__}: {str(exc)[:300]}"
        set_failed(job_id, error_summary)


# ── Endpoints ─────────────────────────────────────────────────────────────────


@router.post(
    "/build",
    response_model=BuildResultResponse,
    summary="Start Knowledge Graph build",
    description=(
        "Ingest documentation files and DDL schemas into Neo4j. "
        "Runs triplet extraction, entity resolution, mapping, and Cypher upsert asynchronously. "
        "Returns a `job_id` — poll **GET /demo/build/{job_id}** for results."
    ),
)
def post_build(req: BuildRequest) -> BuildResultResponse:
    job_id = create_job(meta={"type": "build", "study_id": req.study_id})
    threading.Thread(target=_run_build_task, args=(job_id, req), daemon=True).start()
    return BuildResultResponse(job_id=job_id, status="queued")  # type: ignore[arg-type]


@router.post(
    "/build/upload",
    response_model=BuildResultResponse,
    summary="Start KG build from uploaded files",
    description=(
        "Upload documentation (PDF, MD, TXT) and SQL DDL files directly — "
        "no server-side paths required. "
        "Files are saved to a temporary directory and processed identically to the path-based endpoint. "
        "Returns a `job_id` — poll **GET /demo/build/{job_id}** for results."
    ),
)
async def post_build_upload(
    doc_files: list[UploadFile] = File(..., description="Business documentation files (PDF, MD, TXT)."),
    ddl_files: list[UploadFile] = File(..., description="DDL SQL files to map onto the ontology."),
    clear_graph: bool = True,
    study_id: str = "demo",
    lazy_extraction: bool = False,
) -> BuildResultResponse:
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
        threading.Thread(target=_run_build_task, args=(job_id, req), daemon=True).start()
        return BuildResultResponse(job_id=job_id, status="queued")  # type: ignore[arg-type]
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=400, detail=f"Upload error: {exc}") from exc


@router.get(
    "/build/{job_id}",
    response_model=BuildResultResponse,
    summary="Poll KG build status",
    description=(
        "Poll the result of a build job. "
        "`status` transitions: `queued` → `running` → `done` | `failed`."
    ),
)
def get_build_status(job_id: str) -> BuildResultResponse:
    job = get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail=f"Job '{job_id}' not found.")
    builder = (job.get("result") or {}).get("builder")
    return _build_state_to_response(
        job_id, job["status"], job.get("error"), builder, job.get("current_step")
    )


@router.get(
    "/build/{job_id}/stream",
    summary="Stream KG build progress via Server-Sent Events",
    description=(
        "Opens an SSE stream for a build job. "
        "Emits a JSON event each time the pipeline advances to a new node. "
        "The stream closes automatically when status reaches `done` or `failed`."
    ),
    response_class=__import__("fastapi.responses", fromlist=["StreamingResponse"]).StreamingResponse,
    include_in_schema=True,
)
async def stream_build_status(job_id: str):
    """SSE endpoint — yields JSON events until the job reaches a terminal state."""
    import asyncio
    import json as _json

    from fastapi.responses import StreamingResponse

    async def _event_generator():
        last_step: str | None = "__init__"
        last_status: str = "__init__"
        while True:
            job = get_job(job_id)
            if job is None:
                yield f"data: {_json.dumps({'error': 'job not found'})}\n\n"
                return

            status = job["status"]
            step = job.get("current_step")
            builder = (job.get("result") or {}).get("builder")

            # Emit step/status change events
            if status != last_status or step != last_step:
                last_status = status
                last_step = step
                payload = _build_state_to_response(
                    job_id, status, job.get("error"), builder, step
                ).model_dump()
                yield f"data: {_json.dumps(payload)}\n\n"

            if status in ("done", "failed"):
                return

            await asyncio.sleep(0.5)

    return StreamingResponse(
        _event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",  # disable nginx buffering
        },
    )


@router.post(
    "/query",
    response_model=QueryResponse,
    summary="Answer a question from the Knowledge Graph",
    description=(
        "Synchronous endpoint. Runs hybrid retrieval + cross-encoder reranking + LLM generation "
        "on the currently loaded Neo4j Knowledge Graph. "
        "Requires the KG to be built first via **POST /demo/build**."
    ),
)
def post_query(req: QueryRequest) -> QueryResponse:
    try:
        from src.generation.query_graph import run_query

        env_overrides = req.config.to_env_overrides() if req.config else {}
        with _settings_override(env_overrides):
            result = run_query(req.question, session_id=req.session_id)
        r = _query_result_to_response(result)
        return QueryResponse(
            answer=r.answer,
            sources=r.sources,
            retrieval_quality_score=r.retrieval_quality_score,
            retrieval_chunk_count=r.retrieval_chunk_count,
            gate_decision=r.gate_decision,
            grounded=r.grounded,
            context_previews=r.context_previews,
            session_id=req.session_id,
        )
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail="Internal server error. Check server logs.") from exc


@router.post(
    "/pipeline",
    response_model=PipelineJobResponse,
    summary="Run complete E2E pipeline (build + query)",
    description=(
        "Starts a full end-to-end pipeline: builds the Knowledge Graph from the provided files, "
        "then answers all provided questions asynchronously. "
        "Returns a `job_id` — poll **GET /demo/pipeline/{job_id}** for results."
    ),
)
def post_pipeline(req: PipelineRequest) -> PipelineJobResponse:
    job_id = create_job(
        meta={"type": "pipeline", "study_id": req.study_id, "num_questions": len(req.questions)},
    )
    threading.Thread(target=_run_pipeline_task, args=(job_id, req), daemon=True).start()
    return PipelineJobResponse(job_id=job_id, status="queued", num_questions=len(req.questions))


@router.post(
    "/pipeline/upload",
    response_model=PipelineJobResponse,
    summary="Run complete E2E pipeline from uploaded files",
    description=(
        "Upload docs + DDL files and provide questions as form fields. "
        "Runs a full build + query pipeline asynchronously. "
        "Returns a `job_id` — poll **GET /demo/pipeline/{job_id}** for results."
    ),
)
async def post_pipeline_upload(
    doc_files: list[UploadFile] = File(..., description="Business documentation files (PDF, MD, TXT)."),
    ddl_files: list[UploadFile] = File(..., description="DDL SQL files to map onto the ontology."),
    questions: list[str] = Form(..., description="One or more natural-language questions (send multiple 'questions' fields for a list)."),
    clear_graph: bool = True,
    lazy_extraction: bool = False,
    run_ragas: bool = False,
    study_id: str = "demo",
) -> PipelineJobResponse:
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
        threading.Thread(target=_run_pipeline_task, args=(job_id, req), daemon=True).start()
        return PipelineJobResponse(job_id=job_id, status="queued", num_questions=len(questions))
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=400, detail=f"Upload error: {exc}") from exc


@router.get(
    "/pipeline/{job_id}",
    response_model=PipelineResultResponse,
    summary="Poll E2E pipeline status and results",
    description=(
        "Poll a pipeline job. "
        "When `status='done'`, includes builder metrics and per-question answers."
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
    summary="List all demo jobs",
    description="Returns all submitted build and pipeline jobs with their current status.",
)
def get_demo_jobs() -> list[dict]:
    jobs = [j for j in list_jobs() if j["meta"].get("type") in {"build", "pipeline"}]
    return [
        {
            "job_id": j["job_id"],
            "type": j["meta"].get("type", ""),
            "status": j["status"],
            "study_id": j["meta"].get("study_id", ""),
            "num_questions": j["meta"].get("num_questions"),
        }
        for j in jobs
    ]


@router.delete(
    "/graph",
    summary="Wipe the Knowledge Graph",
    description=(
        "Deletes ALL nodes and relationships from Neo4j (``MATCH (n) DETACH DELETE n``). "
        "This action is irreversible. Requires ``?confirm=true`` query parameter."
    ),
)
def delete_graph(confirm: bool = False) -> dict[str, int]:
    if not confirm:
        raise HTTPException(
            status_code=400,
            detail="Destructive operation — add ?confirm=true to proceed.",
        )
    try:
        from src.graph.neo4j_client import Neo4jClient

        with Neo4jClient() as client:
            count_rows = client.execute_cypher("MATCH (n) RETURN count(n) AS n")
            total = int(count_rows[0].get("n", 0)) if count_rows else 0
            client.execute_cypher("MATCH (n) DETACH DELETE n")
        return {"nodes_deleted": total}
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=503, detail="Neo4j unavailable.") from exc


@router.get(
    "/graph/stats",
    response_model=GraphStatsResponse,
    summary="Current Knowledge Graph statistics",
    description=(
        "Queries Neo4j for live node and relationship counts "
        "across all label types: BusinessConcept, PhysicalTable, ParentChunk, Chunk."
    ),
)
def get_graph_stats() -> GraphStatsResponse:
    try:
        from src.graph.neo4j_client import Neo4jClient

        # Two independent CALL subqueries — no cross-product between nodes and edges
        # Use CALL () { ... } (variable scope clause) required by Neo4j 5.x+
        stats_query = """
        CALL () {
          MATCH (n)
          RETURN
            sum(CASE WHEN 'BusinessConcept' IN labels(n) THEN 1 ELSE 0 END) AS business_concepts,
            sum(CASE WHEN 'PhysicalTable'   IN labels(n) THEN 1 ELSE 0 END) AS physical_tables,
            sum(CASE WHEN 'ParentChunk'     IN labels(n) THEN 1 ELSE 0 END) AS parent_chunks,
            sum(CASE WHEN 'Chunk'           IN labels(n) THEN 1 ELSE 0 END) AS child_chunks,
            count(n) AS total_nodes
        }
        CALL () {
          MATCH ()-[r]->()
          RETURN
            count(r) AS total_relationships,
            sum(CASE WHEN type(r) = 'MENTIONS'   THEN 1 ELSE 0 END) AS mentions_edges,
            sum(CASE WHEN type(r) = 'MAPPED_TO'  THEN 1 ELSE 0 END) AS maps_to_edges,
            sum(CASE WHEN type(r) = 'CHILD_OF'   THEN 1 ELSE 0 END) AS child_of_edges,
            sum(CASE WHEN type(r) = 'REFERENCES' THEN 1 ELSE 0 END) AS references_edges
        }
        RETURN
          business_concepts, physical_tables, parent_chunks, child_chunks, total_nodes,
          total_relationships, mentions_edges, maps_to_edges, child_of_edges, references_edges
        """

        with Neo4jClient() as client:
            row = client.execute_cypher(stats_query)[0]

        return GraphStatsResponse(
            business_concepts=int(row.get("business_concepts", 0) or 0),
            physical_tables=int(row.get("physical_tables", 0) or 0),
            parent_chunks=int(row.get("parent_chunks", 0) or 0),
            child_chunks=int(row.get("child_chunks", 0) or 0),
            mentions_edges=int(row.get("mentions_edges", 0) or 0),
            maps_to_edges=int(row.get("maps_to_edges", 0) or 0),
            child_of_edges=int(row.get("child_of_edges", 0) or 0),
            references_edges=int(row.get("references_edges", 0) or 0),
            total_nodes=int(row.get("total_nodes", 0) or 0),
            total_relationships=int(row.get("total_relationships", 0) or 0),
        )
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=503, detail="Neo4j unavailable.") from exc


def _sanitize_neo4j_value(v: Any) -> Any:
    """Convert Neo4j-native types to JSON-serializable Python primitives."""
    # neo4j.time types: DateTime, Date, Time, Duration
    type_name = type(v).__module__ + "." + type(v).__qualname__
    if "neo4j" in type_name:
        return str(v)
    if isinstance(v, list):
        return [_sanitize_neo4j_value(i) for i in v]
    if isinstance(v, dict):
        return {k2: _sanitize_neo4j_value(v2) for k2, v2 in v.items()}
    return v


@router.get(
    "/graph/data",
    summary="Export Knowledge Graph nodes and edges",
    description=(
        "Returns up to 500 nodes and all their relationships from Neo4j, "
        "formatted for vis-network rendering. Only BusinessConcept and PhysicalTable "
        "nodes (and their direct edges) are included."
    ),
)
def get_graph_data() -> dict:
    try:
        from src.graph.neo4j_client import Neo4jClient

        nodes_query = """
        MATCH (n)
        WHERE n:BusinessConcept OR n:PhysicalTable OR n:ParentChunk OR n:Chunk
        RETURN
          elementId(n) AS id,
          CASE
            WHEN n:PhysicalTable THEN coalesce(n.table_name, toString(elementId(n)))
            WHEN n:ParentChunk   THEN 'P#' + toString(coalesce(n.parent_chunk_index, 0))
            WHEN n:Chunk         THEN 'C#' + toString(coalesce(n.chunk_index, 0))
            ELSE coalesce(n.name, toString(elementId(n)))
          END AS label,
          labels(n)[0]   AS group,
          n.confidence   AS confidence,
          CASE
            WHEN n:BusinessConcept OR n:PhysicalTable THEN properties(n)
            ELSE {
              text:   left(coalesce(n.text, ''), 200),
              source: coalesce(n.source_doc, ''),
              page:   coalesce(n.page, 0)
            }
          END AS props
        LIMIT 800
        """

        edges_query = """
        MATCH (a)-[r]->(b)
        WHERE (a:BusinessConcept OR a:PhysicalTable OR a:ParentChunk OR a:Chunk)
          AND (b:BusinessConcept OR b:PhysicalTable OR b:ParentChunk OR b:Chunk)
        RETURN
          elementId(r)   AS id,
          elementId(a)   AS from_id,
          elementId(b)   AS to_id,
          type(r)        AS label,
          r.confidence   AS confidence
        LIMIT 3000
        """

        with Neo4jClient() as client:
            raw_nodes = client.execute_cypher(nodes_query)
            raw_edges = client.execute_cypher(edges_query)

        nodes = [
            {
                "id": str(row["id"]),
                "label": str(row.get("label") or row["id"]),
                "group": str(row.get("group") or "BusinessConcept"),
                "confidence": int(round((row.get("confidence") or 1.0) * 100))
                if row.get("confidence") is not None
                else None,
                "properties": {
                    k: _sanitize_neo4j_value(v)
                    for k, v in (row.get("props") or {}).items()
                    if k not in ("embedding",)  # omit large vectors
                },
            }
            for row in raw_nodes
        ]

        edges = [
            {
                "id": str(row["id"]),
                "from": str(row["from_id"]),
                "to": str(row["to_id"]),
                "label": str(row.get("label") or ""),
                "confidence": int(round((row.get("confidence") or 1.0) * 100))
                if row.get("confidence") is not None
                else None,
            }
            for row in raw_edges
        ]

        return {"nodes": nodes, "edges": edges}
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=503, detail="Neo4j unavailable.") from exc


# ── KG Snapshot endpoints ─────────────────────────────────────────────────────

@router.get(
    "/kg/snapshots",
    response_model=list[KGSnapshotMeta],
    summary="List saved Knowledge Graph snapshots",
    description="Returns all named KG snapshots stored in the local registry.",
)
def list_kg_snapshots() -> list[KGSnapshotMeta]:
    from src.graph.kg_registry import list_snapshots
    return [KGSnapshotMeta(**s) for s in list_snapshots()]


@router.get(
    "/kg/snapshots/active",
    response_model=KGSnapshotMeta | None,
    summary="Get the currently loaded KG snapshot",
    description="Returns metadata of the active snapshot, or null if none is loaded.",
)
def get_active_kg_snapshot() -> KGSnapshotMeta | None:
    from src.graph.kg_registry import get_active_snapshot
    snap = get_active_snapshot()
    return KGSnapshotMeta(**snap) if snap else None


@router.post(
    "/kg/snapshots",
    response_model=KGSnapshotMeta,
    summary="Save the current KG as a named snapshot",
    description=(
        "Exports the live Neo4j graph to a JSON file and registers it with the given name. "
        "The snapshot can be loaded later via **POST /demo/kg/snapshots/{id}/load**."
    ),
)
def save_kg_snapshot(req: SaveSnapshotRequest) -> KGSnapshotMeta:
    try:
        from src.graph.kg_registry import save_snapshot
        snap = save_snapshot(name=req.name, description=req.description)
        return KGSnapshotMeta(**snap)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail="Internal server error. Check server logs.") from exc


@router.post(
    "/kg/snapshots/{snapshot_id}/load",
    response_model=KGSnapshotMeta,
    summary="Load a saved KG snapshot into Neo4j",
    description=(
        "Clears the current Neo4j graph and restores the selected snapshot. "
        "Equivalent to 'loading a model' — only one KG can be active at a time. "
        "Runs synchronously (may take a few seconds for large graphs)."
    ),
)
def load_kg_snapshot(snapshot_id: str) -> KGSnapshotMeta:
    try:
        from src.graph.kg_registry import load_snapshot
        snap = load_snapshot(snapshot_id)
        return KGSnapshotMeta(**snap)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except FileNotFoundError as exc:
        raise HTTPException(status_code=410, detail=str(exc)) from exc
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail="Internal server error. Check server logs.") from exc


@router.post(
    "/kg/snapshots/eject",
    summary="Eject the active KG snapshot",
    description=(
        "Clears the active-snapshot pointer without modifying Neo4j. "
        "Use this to signal that no named snapshot is currently loaded."
    ),
)
def eject_kg_snapshot() -> dict[str, str]:
    from src.graph.kg_registry import eject_snapshot
    eject_snapshot()
    return {"status": "ejected"}


@router.delete(
    "/kg/snapshots/{snapshot_id}",
    summary="Delete a saved KG snapshot",
    description="Removes the snapshot file and its registry entry. Cannot be undone.",
)
def delete_kg_snapshot(snapshot_id: str) -> dict[str, str]:
    try:
        from src.graph.kg_registry import delete_snapshot
        delete_snapshot(snapshot_id)
        return {"status": "deleted", "id": snapshot_id}
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail="Internal server error. Check server logs.") from exc


@router.patch(
    "/kg/snapshots/{snapshot_id}",
    response_model=KGSnapshotMeta,
    summary="Rename / update a KG snapshot",
    description="Update the name and/or description of an existing snapshot.",
)
def rename_kg_snapshot(snapshot_id: str, req: RenameSnapshotRequest) -> KGSnapshotMeta:
    try:
        from src.graph.kg_registry import rename_snapshot
        snap = rename_snapshot(snapshot_id, req.name, req.description)
        return KGSnapshotMeta(**snap)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail="Internal server error. Check server logs.") from exc


# ── Conversation endpoints ────────────────────────────────────────────────────

@router.get(
    "/conversations",
    response_model=list[ConversationMeta],
    summary="List saved conversations",
    description="Returns all saved chat conversations ordered by last update.",
)
def list_conversations() -> list[ConversationMeta]:
    from src.graph.conversation_registry import list_conversations as _list
    return [ConversationMeta(**c) for c in _list()]


@router.get(
    "/conversations/{conversation_id}",
    response_model=ConversationDetail,
    summary="Get a saved conversation",
    description="Returns the full message history for a saved conversation.",
)
def get_conversation(conversation_id: str) -> ConversationDetail:
    from pydantic import ValidationError

    from src.graph.conversation_registry import get_conversation as _get
    try:
        conv = _get(conversation_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    try:
        return ConversationDetail(**conv)
    except ValidationError as exc:
        raise HTTPException(status_code=500, detail="Stored conversation data is corrupted.") from exc


@router.post(
    "/conversations",
    response_model=ConversationMeta,
    summary="Save a conversation",
    description="Persist a chat conversation (session ID + messages) for later retrieval.",
)
def save_conversation(req: SaveConversationRequest) -> ConversationMeta:
    from src.graph.conversation_registry import save_conversation as _save
    try:
        conv = _save(
            session_id=req.session_id,
            title=req.title,
            messages=[m.model_dump() for m in req.messages],
            active_snapshot_id=req.active_snapshot_id,
        )
        return ConversationMeta(**conv)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail="Internal server error. Check server logs.") from exc


@router.patch(
    "/conversations/{conversation_id}",
    response_model=ConversationMeta,
    summary="Rename a conversation",
    description="Update the title of a saved conversation.",
)
def rename_conversation(conversation_id: str, req: RenameConversationRequest) -> ConversationMeta:
    from src.graph.conversation_registry import rename_conversation as _rename
    try:
        conv = _rename(conversation_id, req.title)
        return ConversationMeta(**conv)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail="Internal server error. Check server logs.") from exc


@router.delete(
    "/conversations/{conversation_id}",
    summary="Delete a conversation",
    description="Remove a saved conversation permanently.",
)
def delete_conversation(conversation_id: str) -> dict[str, str]:
    from src.graph.conversation_registry import delete_conversation as _delete
    try:
        _delete(conversation_id)
        return {"status": "deleted", "id": conversation_id}
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail="Internal server error. Check server logs.") from exc

