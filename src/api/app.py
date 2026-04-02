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
## APIs

### E2E Demo  `/api/v1/demo/`
Drive the full GraphRAG pipeline interactively:
- **POST `/demo/build`** — start an async Knowledge Graph build
- **GET `/demo/build/{job_id}`** — poll build progress
- **POST `/demo/query`** — answer a question synchronously from the KG
- **POST `/demo/pipeline`** — full async E2E: build + multi-question answering
- **GET `/demo/pipeline/{job_id}`** — poll pipeline results
- **GET `/demo/graph/stats`** — live Neo4j node/edge counts

### Ablation Studies  `/api/v1/ablation/`
Run, monitor and compare ablation experiments:
- **POST `/ablation/run/preset`** — launch a predefined AB-XX study (matrix config auto-applied)
- **POST `/ablation/run/custom`** — launch a fully custom run (any flags + hyperparameters)
- **GET `/ablation/status/{job_id}`** — poll status and metrics
- **GET `/ablation/jobs`** — list all submitted jobs
- **GET `/ablation/matrix`** — browse the 21 predefined AB-00…AB-20 conditions
- **GET `/ablation/datasets`** — list available gold-standard evaluation fixtures
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
