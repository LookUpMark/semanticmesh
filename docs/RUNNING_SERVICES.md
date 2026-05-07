# Running the Thesis Project - Services & Setup Guide

This guide explains how to set up and run all services required for the Multi-Agent Framework for Semantic Discovery & GraphRAG.

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Neo4j Database Setup](#neo4j-database-setup)
3. [Environment Configuration](#environment-configuration)
4. [Running the API Server](#running-the-api-server)
5. [Running the Pipeline (CLI)](#running-the-pipeline-cli)
6. [Development Setup](#development-setup)
7. [Troubleshooting](#troubleshooting)

---

## Quick Start

```bash
# 1. Start Neo4j with Docker
docker run -d --name thesis-neo4j \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/thesis_password \
  -v neo4j-thesis-data:/data \
  neo4j:5

# 2. Configure environment
cp .env.example .env
# Edit .env — set OPENAI_API_KEY (or another provider) and API_KEY

# 3. Install dependencies
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# 4. Start the API server
python -m scripts.serve_api

# 5. Open Swagger UI
xdg-open http://127.0.0.1:8000/docs
```

---

## 🗄️ Neo4j Database Setup

### Why Neo4j?

The Multi-Agent Framework uses Neo4j as its knowledge graph storage because:
- **Native graph database** - Optimized for traversing relationships
- **Cypher query language** - Powerful, SQL-like language for graphs
- **Vector indexing** - Supports hybrid vector + graph queries

### Option 1: Docker

#### Start a new Neo4j container:

```bash
docker run -d \
  --name neo4j-thesis \
  -p 7474:7474 \
  -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/your_password_here \
  -v neo4j-data:/data \
  neo4j:5
```

**What this does:**
- `-d` - Run in detached mode (background)
- `--name neo4j-thesis` - Name the container for easy management
- `-p 7474:7474` - Expose Neo4j Browser (web UI) on port 7474
- `-p 7687:7687` - Expose Bolt protocol (database connection) on port 7687
- `-e NEO4J_AUTH` - Set username/password
- `-v neo4j-data:/data` - Persist data in a named volume

#### Neo4j Browser UI:

Once running, access the Neo4j Browser at:
- **URL:** http://localhost:7474
- **Username:** `neo4j`
- **Password:** `your_password_here`

#### Docker Management Commands:

```bash
# Check if Neo4j is running
docker ps | grep neo4j-thesis

# View Neo4j logs
docker logs neo4j-thesis

# Stop Neo4j
docker stop neo4j-thesis

# Start Neo4j (stopped container)
docker start neo4j-thesis

# Remove Neo4j container (WARNING: deletes data)
docker rm -f neo4j-thesis
```

> **Note:** Docker is used here only for Neo4j. The backend API runs natively.

### Option 2: Neo4j Desktop

1. Download [Neo4j Desktop](https://neo4j.com/download/)
2. Install and open Neo4j Desktop
3. Create a new project
4. Add a local database (version 5.x)
5. Set username: `neo4j` and your chosen password
6. Start the database
7. Note the Bolt URL (usually `bolt://localhost:7687`)

### Option 3: Neo4j AuraDB (Cloud - Free Tier)

1. Visit [Neo4j Aura](https://neo4j.com/cloud-platform/aura-free/)
2. Create a free account
3. Create a new AuraDB Free instance
4. Copy the connection string (Bolt URI)
5. Use the AuraDB credentials in your `.env` file

---

## Environment Configuration

### Create `.env` File

```bash
cp .env.example .env
```

### Required Configuration

Edit `.env` with your values:

```bash
# ── Neo4j (must match your Docker container) ────────────────────────
NEO4J_USER=neo4j
NEO4J_PASSWORD=thesis_password

# ── LLM API Key (at least one required) ─────────────────────────────
OPENAI_API_KEY=sk-proj-...

# ── API Authentication ───────────────────────────────────────────────
# Generate: python -c "import secrets; print(secrets.token_urlsafe(32))"
API_KEY=your-generated-key
```

### Optional Overrides

```bash
# Model selection (defaults to gpt-4.1 family)
LLM_MODEL_REASONING=gpt-4.1
LLM_MODEL_EXTRACTION=gpt-4.1-nano
LLM_MODEL_MIDTIER=gpt-4.1-nano

# Retrieval tuning
RETRIEVAL_VECTOR_TOP_K=20
RERANKER_TOP_K=5

# Feature flags (disable for ablation testing)
ENABLE_CYPHER_HEALING=false
ENABLE_HALLUCINATION_GRADER=false
```

See [.env.example](../.env.example) for the full list of supported variables.

---

## Running the API Server

The primary interface to SemanticMesh is the FastAPI REST API.

### Start the Server

```bash
source .venv/bin/activate
set -a && source .env && set +a    # Load environment variables

# Production mode (single worker)
python -m scripts.serve_api

# Development mode (auto-reload on code changes)
python -m scripts.serve_api --reload

# Custom port / host
python -m scripts.serve_api --host 0.0.0.0 --port 9000

# Multiple workers (no --reload)
python -m scripts.serve_api --workers 4
```

### Available Services

| Service | URL | Auth |
|---------|-----|------|
| Swagger UI (interactive) | http://localhost:8000/docs | — |
| ReDoc (read-only) | http://localhost:8000/redoc | — |
| OpenAPI JSON | http://localhost:8000/openapi.json | — |
| Health check | http://localhost:8000/health | No |
| All `/api/v1/*` endpoints | http://localhost:8000/api/v1/... | Yes (`X-API-Key` header) |

### Authentication

When `API_KEY` is set in `.env`, all `/api/v1/*` endpoints require the `X-API-Key` header:

```bash
# Generate a secure key
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Use in requests
curl -H "X-API-Key: YOUR_KEY" http://localhost:8000/api/v1/demo/graph/stats
```

In Swagger UI, click the **Authorize** button (lock icon) and paste your key once — it's included in all subsequent requests.

When `API_KEY` is **not set**, auth is disabled (dev mode). A warning banner is logged at startup.

### API Endpoint Groups

**Demo Pipeline (`/api/v1/demo/`)**
- `POST /demo/build` — Start KG build from server-side paths
- `POST /demo/build/upload` — Start KG build from uploaded files
- `GET /demo/build/{job_id}` — Poll build status
- `GET /demo/build/{job_id}/stream` — SSE stream of build progress
- `POST /demo/query` — Synchronous Q&A against loaded KG
- `POST /demo/pipeline` — Full E2E: build KG + answer questions
- `POST /demo/pipeline/upload` — Same with file uploads
- `GET /demo/pipeline/{job_id}` — Poll pipeline results
- `GET /demo/jobs` — List all demo jobs
- `DELETE /demo/graph?confirm=true` — Wipe KG (requires API_KEY)
- `GET /demo/graph/stats` — Live Neo4j node/edge counts
- `GET /demo/graph/data` — Export nodes+edges for visualization

**KG Snapshots (`/api/v1/demo/kg/`)**
- `GET /demo/kg/snapshots` — List saved snapshots
- `GET /demo/kg/snapshots/active` — Currently loaded snapshot
- `POST /demo/kg/snapshots` — Save current KG
- `POST /demo/kg/snapshots/{id}/load` — Load a snapshot into Neo4j
- `POST /demo/kg/snapshots/eject` — Unmark active snapshot
- `PATCH /demo/kg/snapshots/{id}` — Rename snapshot
- `DELETE /demo/kg/snapshots/{id}` — Delete snapshot

**Conversations (`/api/v1/demo/conversations/`)**
- `GET /demo/conversations` — List saved conversations
- `GET /demo/conversations/{id}` — Get full conversation
- `POST /demo/conversations` — Save a conversation
- `PATCH /demo/conversations/{id}` — Rename
- `DELETE /demo/conversations/{id}` — Delete

**Ablation Studies (`/api/v1/ablation/`)**
- `GET /ablation/matrix` — Browse 21+ predefined AB-XX studies
- `GET /ablation/datasets` — List available evaluation datasets
- `POST /ablation/run/preset` — Launch predefined study
- `POST /ablation/run/custom` — Launch custom study
- `GET /ablation/status/{job_id}` — Poll status and results
- `GET /ablation/jobs` — List all ablation jobs
- `GET /ablation/bundle/{study_id}/{dataset_id}` — Download evaluation bundle
- `GET /ablation/evaluate/{study_id}/{dataset_id}` — AI Judge payload

**Configuration (`/api/v1/config`)**
- `GET /config` — View current runtime settings (non-sensitive)
- `POST /config` — Override settings at runtime (no restart needed)

---

## Running the Pipeline (CLI)

For batch evaluation and ablation studies, use the CLI scripts:

```bash
source .venv/bin/activate
set -a && source .env && set +a

# Run AB-BEST on all 6 datasets (auto-manages Neo4j container)
pipeline-run --best --all-datasets --auto-neo4j

# Run a specific ablation study
pipeline-run --study AB-03 --dataset 01

# Run AI Judge on all completed bundles
ai-judge --all

# Run AI Judge on specific study/dataset
ai-judge --studies AB-BEST --datasets 01,02,03
```

---

## Development Setup

### Python Environment

```bash
# Create virtual environment (if not exists)
python -m venv .venv

# Activate
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# Install with development dependencies
pip install -e ".[dev]"

# Verify
python --version           # Requires 3.11+
pytest tests/unit/ -q      # Should pass 500+ tests
```

### Running Tests

```bash
# Unit tests (no Neo4j needed)
pytest tests/unit/ -v

# Integration tests (Neo4j must be running)
pytest tests/integration/ -v

# All tests with coverage
pytest tests/ --cov=src --cov-report=html

# Specific test file
pytest tests/unit/test_settings.py -v
```

### Linting and Formatting

```bash
ruff check src/ tests/             # Lint
ruff check --fix src/ tests/       # Auto-fix
ruff format src/ tests/            # Format
mypy src/                          # Type check
```

---

## Troubleshooting

### Neo4j Connection Issues

**Problem:** `ServiceUnavailable: Unable to connect to bolt://localhost:7687`

**Solutions:**
1. Verify Neo4j is running: `docker ps | grep thesis-neo4j`
2. Check Neo4j logs: `docker logs thesis-neo4j`
3. Verify port 7687 is not in use: `lsof -i :7687`
4. Ensure credentials match `.env`

### LLM API Issues

**Problem:** `AuthenticationError: Invalid API key`

**Solutions:**
1. Verify `.env` file exists and is sourced: `set -a && source .env && set +a`
2. Check `OPENAI_API_KEY` is set correctly (no extra spaces)
3. Test with curl:
   ```bash
   curl -s https://api.openai.com/v1/models \
     -H "Authorization: Bearer $OPENAI_API_KEY" | head -c 200
   ```

### Import Errors

**Problem:** `ModuleNotFoundError: No module named 'src'`

**Solutions:**
1. Install in editable mode: `pip install -e .`
2. Verify you're in the project root directory
3. Use `.venv/bin/python` explicitly (system python won't have project packages)

### API Server Issues

**Problem:** Server won't start / endpoints return 500

**Solutions:**
1. Ensure `.env` is sourced before starting: `set -a && source .env && set +a`
2. Check Neo4j is running (graph endpoints need it)
3. View server logs (stdout/stderr from uvicorn)
4. Try with `--reload` for better error reporting during development

### GPU / Embedding Issues

**Problem:** Slow embedding or reranker

**Solutions:**
1. Verify CUDA is available: `python -c "import torch; print(torch.cuda.is_available())"`
2. BGE-M3 and bge-reranker-v2-m3 auto-detect GPU on first call
3. First query is slow (model loading) — subsequent queries are fast

---

## Observability (LangSmith + Langfuse)

SemanticMesh supports dual observability backends for tracing every LLM call, chain invocation, and LangGraph node execution. Both are **opt-in** — if the keys are not set, the system runs with zero overhead.

### LangSmith (LangChain native)

LangSmith is automatically enabled by LangChain/LangGraph when the following environment variables are set:

```bash
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=ls-...          # Get from https://smith.langchain.com
LANGCHAIN_PROJECT=semanticmesh    # Optional (defaults to "default")
```

**What gets traced:**
- Every LLM `.invoke()` / `.ainvoke()` call (model, prompt, response, tokens, latency)
- LangGraph node transitions and state
- Full chain-of-thought for multi-step pipelines

**Dashboard:** https://smith.langchain.com

### Langfuse (open-source alternative)

Langfuse provides the same tracing capabilities with a self-hostable, open-source dashboard.

```bash
LANGFUSE_PUBLIC_KEY=pk-lf-...     # Get from https://cloud.langfuse.com or self-hosted
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_HOST=https://cloud.langfuse.com   # Or your self-hosted URL
```

**What gets traced:**
- All LLM calls via `LangchainCallbackHandler` (injected automatically in `InstrumentedLLM`)
- Cost tracking, token usage, latency histograms
- Evaluation scores (if integrated with Langfuse evaluations)

**Dashboard:** https://cloud.langfuse.com (or self-hosted)

### Both Together

You can enable both simultaneously. LangSmith traces via LangChain's internal hooks (env-var-based), while Langfuse uses an explicit callback handler injected into each LLM call.

```bash
# .env — enable both
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=ls-...
LANGCHAIN_PROJECT=semanticmesh
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_HOST=https://cloud.langfuse.com
```

### Architecture

```
┌─────────────────────────────────────────────────┐
│  Pipeline Node (extraction, generation, etc.)   │
└────────────────────┬────────────────────────────┘
                     │ invoke()
                     ▼
┌─────────────────────────────────────────────────┐
│            InstrumentedLLM                       │
│  ┌──────────────────────────────────────────┐   │
│  │ _inject_observability_callbacks(kwargs)   │   │
│  │  → Merges Langfuse CallbackHandler        │   │
│  └──────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────┐   │
│  │ Retry logic + latency/token logging       │   │
│  └──────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────┘
                     │ model.invoke(input, config={"callbacks": [...]})
                     ▼
┌─────────────────────────────────────────────────┐
│  LangChain BaseChatModel (ChatOpenAI, etc.)     │
│  ┌───────────┐  ┌─────────────┐                │
│  │ LangSmith │  │  Langfuse   │  ← callbacks   │
│  │  (auto)   │  │ (explicit)  │                │
│  └───────────┘  └─────────────┘                │
└─────────────────────────────────────────────────┘
```

### Verification

After setting environment variables, check the server startup logs:

```
INFO  Observability: LangSmith tracing ENABLED
INFO  Observability: Langfuse tracing ENABLED
```

Or test programmatically:

```python
from src.config.observability import is_langsmith_enabled, is_langfuse_enabled
print("LangSmith:", is_langsmith_enabled())
print("Langfuse:", is_langfuse_enabled())
```

---

## Additional Resources

- **Project README:** [`README.md`](../README.md)
- **Ablation Results:** [`docs/ablation/RESULTS.md`](ablation/RESULTS.md)
- **API Swagger UI:** http://localhost:8000/docs
- **Neo4j Browser:** http://localhost:7474
- **LangGraph Docs:** https://langchain-ai.github.io/langgraph/
- **Neo4j Docs:** https://neo4j.com/docs/

---

## 🆘 Getting Help

If you encounter issues not covered here:

1. Check the [GitHub Issues](https://github.com/your-repo/issues)
2. Review the test files in `tests/unit/` for usage examples
3. Enable debug logging in `.env`:
   ```bash
   LOG_LEVEL=DEBUG
   ```
4. Check the logs for detailed error messages

---

**Last updated:** April 2026
