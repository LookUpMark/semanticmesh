"""FastAPI application — mounts both the E2E Demo and Ablation Studies APIs."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.ablation_router import router as ablation_router
from src.api.demo_router import router as demo_router

app = FastAPI(
    title="GraphRAG Thesis API",
    version="1.0.0",
    summary=(
        "Multi-Agent Framework for Semantic Discovery & GraphRAG — "
        "REST interface for end-to-end demos and ablation studies."
    ),
    description="""
## E2E Demo  `/api/v1/demo/`

Drive the full GraphRAG pipeline interactively:

**KG Build**
- `POST /demo/build` — start async KG build from server-side file paths
- `POST /demo/build/upload` — start async KG build from uploaded files (no server paths needed)
- `GET  /demo/build/{job_id}` — poll build status and metrics

**Query**
- `POST /demo/query` — answer a question synchronously from the current KG

**Full Pipeline (build + query)**
- `POST /demo/pipeline` — start full async E2E pipeline from server-side paths
- `POST /demo/pipeline/upload` — start full async E2E from uploaded files
- `GET  /demo/pipeline/{job_id}` — poll pipeline status and per-question answers

**Utility**
- `GET /demo/jobs` — list all submitted build/pipeline jobs
- `GET /demo/graph/stats` — live Neo4j node/edge counts

---

## Ablation Studies  `/api/v1/ablation/`

Run, monitor, and compare ablation experiments:

**Reference**
- `GET /ablation/matrix` — browse 21 predefined AB-00…AB-20 conditions
- `GET /ablation/datasets` — list available gold-standard evaluation fixtures

**Launch**
- `POST /ablation/run/preset` — launch a predefined AB-XX study (flags auto-applied from matrix)
- `POST /ablation/run/custom` — launch a fully custom run (any flags + hyperparameters)

**Monitor**
- `GET /ablation/status/{job_id}` — poll status, summary metrics, and RAGAS scores
- `GET /ablation/jobs` — list all submitted ablation jobs

**Results**
- `GET /ablation/bundle/{study_id}/{dataset_id}` — download full evaluation bundle JSON
- `GET /ablation/evaluate/{study_id}/{dataset_id}` — AI-as-Judge payload (system prompt + bundle)
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Allow all origins in development (tighten for production if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(demo_router, prefix="/api/v1")
app.include_router(ablation_router, prefix="/api/v1")


@app.get("/health", tags=["Health"])
def health() -> dict[str, str]:
    """Liveness probe — returns 200 OK when the server is up."""
    return {"status": "ok"}
