# SemanticMesh

[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Neo4j 5.x](https://img.shields.io/badge/Neo4j-5.x-018BFF.svg)](https://neo4j.com/)
[![LangGraph](https://img.shields.io/badge/LangGraph-orchestrated-1C3C3C.svg)](https://langchain-ai.com/langgraph/)

A LangGraph-orchestrated multi-agent system for automated Data Governance. Bridges unstructured business documentation (PDF/TXT) with relational database schemas (DDL/SQL) by constructing a Knowledge Graph on Neo4j and answering natural-language queries against it.

Master's thesis, Politecnico di Torino, March 2026.

---

## Table of Contents

- [Architecture](#architecture)
- [Key Features](#key-features)
- [Getting Started](#getting-started)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Evaluation](#evaluation)
- [Documentation](#documentation)
- [License](#license)

---

## Architecture

Data Governance requires aligning business semantics (expressed in free-text glossaries, data dictionaries, and process descriptions) with the physical structures of relational databases. This alignment is traditionally performed manually by data stewards, a process that is error-prone, time-consuming, and does not scale.

This project proposes a generative AI framework that automates this alignment through two coordinated LangGraph pipelines:

1. **Builder Graph** -- Ingests business documents and DDL schemas, extracts semantic triplets, resolves entities, maps business concepts to physical tables, and upserts the resulting ontology into a Neo4j Knowledge Graph.

2. **Query Graph** -- Answers natural-language questions against the Knowledge Graph using hybrid retrieval (dense vector + BM25 + graph traversal), cross-encoder reranking, and hallucination-graded answer generation.

The system employs self-reflection loops (Actor-Critic validation, Cypher healing), a provider-agnostic multi-tier LLM factory, and a comprehensive ablation study framework (21 studies across 7 datasets) to quantify the marginal contribution of each architectural component.

### Two-Graph Pipeline

#### Builder Graph

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#FAFAFA', 'primaryTextColor': '#212121', 'primaryBorderColor': '#9E9E9E', 'lineColor': '#616161', 'fontSize': '13px', 'fontFamily': 'Inter, Helvetica, Arial, sans-serif'}}}%%
flowchart TD
    A("Business Documents<br/>PDF / TXT"):::input
    B("DDL Schemas<br/>SQL"):::input
    C("Triplet Extraction<br/>SLM"):::process
    D("DDL Parse + Schema Enrichment<br/>LLM-expanded identifiers"):::process
    E("Entity Resolution<br/>K-NN blocking + LLM Judge"):::key
    PM("Parallel Mapping<br/>ThreadPool × N tables"):::key
    F("RAG Mapping<br/>Map-Reduce per table"):::process
    G("Actor-Critic Validation<br/>Structured critique"):::key
    H("HITL Interrupt<br/>Low confidence"):::optional
    I("Cypher Generation<br/>CREATE / MERGE"):::process
    J("Cypher Healing<br/>EXPLAIN dry-run + LLM fix"):::key
    K("Neo4j Upsert<br/>MERGE + FK edges + embeddings"):::process
    L[("Neo4j<br/>Knowledge Graph")]:::database

    A --> C
    B --> D
    C --> E
    E --> PM
    D --> PM
    PM --> F
    F --> G
    G -- "rejected" --> F
    G -. "conf < gate" .-> H
    H --> I
    G -- "approved" --> I
    I --> J
    J -- "EXPLAIN failed" --> I
    J -- "valid" --> K
    K --> L
    K -. "next table" .-> F

    classDef input fill:#FAFAFA,stroke:#424242,stroke-width:2px
    classDef process fill:#F5F5F5,stroke:#9E9E9E,stroke-width:1.5px
    classDef key fill:#E3F2FD,stroke:#1565C0,stroke-width:2px,color:#0D47A1
    classDef optional fill:#FAFAFA,stroke:#9E9E9E,stroke-width:1.5px,stroke-dasharray: 5 5
    classDef database fill:#37474F,stroke:#263238,stroke-width:2px,color:#ECEFF1
```

#### Query Graph

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#FAFAFA', 'primaryTextColor': '#212121', 'primaryBorderColor': '#9E9E9E', 'lineColor': '#616161', 'fontSize': '13px', 'fontFamily': 'Inter, Helvetica, Arial, sans-serif'}}}%%
flowchart TD
    A("Natural Language Question"):::input
    B("Hybrid Retrieval<br/>Dense + BM25 + Graph Traversal"):::process
    C("Cross-Encoder Reranking"):::process
    D{"Retrieval<br/>Quality Gate"}:::gate
    E("Context Distillation<br/>adequate / sparse / insufficient"):::process
    F("Answer Generation<br/>Context-adaptive"):::process
    G("Hallucination Grader<br/>Self-RAG structured critique"):::key
    H("Grader Consistency Validator"):::key
    I("Grounded Answer + Sources"):::output
    J("Abstain<br/>Insufficient context"):::optional

    A --> B
    B --> C
    C --> D
    D -- "proceed" --> E
    D -. "abstain" .-> J
    E --> F
    F --> G
    G --> H
    H -- "regenerate" --> F
    H -- "pass" --> I

    classDef input fill:#FAFAFA,stroke:#424242,stroke-width:2px
    classDef process fill:#F5F5F5,stroke:#9E9E9E,stroke-width:1.5px
    classDef key fill:#E3F2FD,stroke:#1565C0,stroke-width:2px,color:#0D47A1
    classDef gate fill:#FAFAFA,stroke:#424242,stroke-width:2px
    classDef output fill:#37474F,stroke:#263238,stroke-width:2px,color:#ECEFF1
    classDef optional fill:#FAFAFA,stroke:#9E9E9E,stroke-width:1.5px,stroke-dasharray: 5 5
```

### Builder Graph

| Stage | Module | Description |
|-------|--------|-------------|
| Ingestion | `ingestion/pdf_loader`, `ddl_parser` | Load PDF/TXT documents, parse DDL schemas via sqlglot |
| Schema Enrichment | `ingestion/schema_enricher` | LLM expands abbreviated identifiers (e.g. `TB_CST` to `Customer Table`) |
| Triplet Extraction | `extraction/triplet_extractor` | SLM extracts `(subject, predicate, object)` triplets in JSON mode |
| Entity Resolution | `resolution/blocking` + `llm_judge` | Two-stage: K-NN blocking with BGE-M3 embeddings, then LLM judge decides merge/separate |
| Parallel Mapping | `graph/parallel_mapping` | ThreadPool pre-computes mapping+validation for all tables concurrently (5 workers) |
| RAG Mapping | `mapping/rag_mapper` + `validator` | Map-Reduce RAG per table with Actor-Critic validation loop |
| HITL | `mapping/hitl` | LangGraph interrupt for low-confidence mappings |
| Graph Build | `graph/cypher_generator` + `cypher_healer` | LLM generates Cypher, EXPLAIN dry-run validates, auto-healing on syntax errors |
| Upsert | `graph/build_nodes` + `cypher_builder` | MERGE upserts + FK edge construction + duplicate concept handling |

### Query Graph

| Stage | Module | Description |
|-------|--------|-------------|
| Hybrid Retrieval | `retrieval/hybrid_retriever` | Dense (BGE-M3) + BM25 + graph traversal, fused via Reciprocal Rank Fusion |
| Reranking | `retrieval/reranker` | Cross-encoder reranking with bge-reranker-v2-m3 |
| Context Assessment | `generation/context_distiller` | Evaluates context sufficiency (adequate/sparse/insufficient) |
| Answer Generation | `generation/answer_generator` | Context-adaptive LLM generation with critique injection on retry |
| Hallucination Grading | `generation/hallucination_grader` | Self-RAG grader emitting structured critiques |

---

## Key Features

- **Provider-agnostic LLM factory** -- Supports OpenRouter, OpenAI, Anthropic, Google, Ollama, LM Studio, and more. Auto-detects provider from model name.
- **5-tier model routing** -- Nano (lightweight tasks), extraction (JSON mode), midtier (mapping/grading), generation (T=0.3), reasoning (complex tasks).
- **Parallel mapping** -- ThreadPoolExecutor-based concurrent mapping+validation (configurable workers), ~5x speedup on large schemas (50+ tables).
- **Self-reflection loops** -- Actor-Critic mapping validation with best-proposal tracking; Cypher healing with deterministic fallback builder.
- **Hybrid retrieval with RRF** -- Dense (BGE-M3) + BM25 + graph traversal, fused via Reciprocal Rank Fusion, followed by cross-encoder reranking.
- **Hierarchical chunking** -- Small-to-Big retrieval pattern for context-rich answer generation.
- **Human-in-the-loop** -- LangGraph interrupts for low-confidence mapping decisions.
- **Incremental ingestion** -- SHA-256 change detection skips unchanged documents.
- **UNWIND batch writes** -- ~87% Neo4j write reduction over individual MERGE operations.
- **Confidence gating** -- Skip expensive critic inference when confidence >= 0.85.
- **Comprehensive ablation framework** -- 21 studies across 7 synthetic datasets with automated AI Judge evaluation.
- **REST API** -- FastAPI endpoints for demo pipeline execution and ablation study management.

---

## Getting Started

### Prerequisites

| Requirement | Version | Notes |
|-------------|---------|-------|
| Python | 3.11+ | 3.12 recommended |
| Neo4j | 5.x | Docker recommended (only external service) |
| LLM API key | — | At least one: OpenAI, Anthropic, OpenRouter, or local (Ollama/LM Studio) |
| Docker | 20+ | Only for Neo4j |
| GPU (optional) | CUDA 11.8+ | Accelerates embedding (BGE-M3) and reranker (bge-reranker-v2-m3) |

### Step 1: Clone & Install

```bash
git clone https://github.com/LookUpMark/semanticmesh.git
cd semanticmesh

# Create virtual environment
python3.12 -m venv .venv
source .venv/bin/activate

# Install all dependencies (includes langfuse, langgraph, sentence-transformers, etc.)
pip install -e ".[dev]"
```

### Step 2: Start Neo4j

```bash
docker run -d --name thesis-neo4j \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/your_password_here \
  -v neo4j-thesis-data:/data \
  neo4j:5
```

Verify: open http://localhost:7474 → login with `neo4j` / `your_password_here`.

### Step 3: Get LLM API Keys

You need **at least one** LLM provider. Recommended: **OpenAI** (best quality for this project).

| Provider | Sign up | Key format |
|----------|---------|------------|
| OpenAI | https://platform.openai.com/signup → API Keys | `sk-proj-...` |
| OpenRouter | https://openrouter.ai → Keys | `sk-or-v1-...` |
| Anthropic | https://console.anthropic.com → API Keys | `sk-ant-...` |
| Ollama (local) | https://ollama.com → Install → `ollama pull llama3.1` | No key needed |

### Step 4: Configure Environment

```bash
cp .env.example .env
```

Edit `.env` with your values:

```dotenv
# ── Required ─────────────────────────────────────────────────────────────────
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password_here        # Must match Docker -e NEO4J_AUTH

OPENAI_API_KEY=sk-proj-...               # At least one LLM key

# Generate a secure API key for the REST API:
# python -c "import secrets; print(secrets.token_urlsafe(32))"
API_KEY=your-generated-key

# ── Optional: Model Selection ────────────────────────────────────────────────
LLM_MODEL_REASONING=gpt-4.1             # For complex reasoning/judge tasks
LLM_MODEL_EXTRACTION=gpt-4.1-nano       # For triplet extraction (fast + cheap)
LLM_MODEL_MIDTIER=gpt-4.1-nano          # For schema enrichment, mapping
```

### Step 5: Start the API Server

```bash
source .venv/bin/activate
set -a && source .env && set +a          # Load env vars into shell

python -m scripts.serve_api              # http://127.0.0.1:8000
python -m scripts.serve_api --reload     # Dev mode (auto-reload on code changes)
```

| Service | URL |
|---------|-----|
| Swagger UI (interactive docs) | http://localhost:8000/docs |
| ReDoc (read-only docs) | http://localhost:8000/redoc |
| Health check | http://localhost:8000/health |
| Neo4j Browser | http://localhost:7474 |

### Step 6: Verify Installation

```bash
# Health check (no auth)
curl http://localhost:8000/health
# → {"status": "ok"}

# Authenticated request (requires API_KEY)
curl -H "X-API-Key: YOUR_KEY" http://localhost:8000/api/v1/demo/graph/stats
# → {"nodes": 0, "relationships": 0, ...}
```

### Step 7 (Optional): Enable Observability

#### LangSmith — Pipeline tracing & visualization

1. **Sign up**: https://smith.langchain.com (free with GitHub/Google)
2. Go to **Settings → API Keys** → Create API Key → copy `lsv2_pt_...`
3. (Optional) Create a project named "semanticmesh" in **Projects**
4. Add to `.env`:

```dotenv
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=lsv2_pt_...
LANGCHAIN_PROJECT=semanticmesh
```

**Free tier**: 5,000 traces/month, 14-day retention.
**Dashboard**: https://smith.langchain.com → Projects → semanticmesh

#### Langfuse — Cost analytics & open-source tracing

1. **Sign up**: https://cloud.langfuse.com (free with GitHub/Google/email)
2. Create a new **Project** (e.g. "semanticmesh")
3. Go to **Settings → API Keys** → Create new API keys
4. Copy both `Public Key` (pk-lf-...) and `Secret Key` (sk-lf-...)
5. Add to `.env`:

```dotenv
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_HOST=https://cloud.langfuse.com
```

**Hobby tier (free)**: 50k observations/month, all features, no credit card.
**Dashboard**: https://cloud.langfuse.com

#### LangGraph Studio — Interactive graph visualization

```bash
# Install CLI (already included in dev dependencies)
pip install "langgraph-cli[inmem]"

# Start Studio dev server
set -a && source .env && set +a
langgraph dev

# Open in browser:
# https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024
```

Requires a LangSmith account (uses LANGCHAIN_API_KEY). Shows animated graph execution, state inspection, and step-through debugging.


---

## Configuration

The application uses a two-tier configuration system:

1. **`src/config/config.py`** -- Non-sensitive defaults (dataclass). All defaults are visible in code and overridable via environment variables.
2. **`.env`** -- Sensitive values only (API keys, passwords). See [.env.example](.env.example) for the full template.

All 70+ settings are documented in [.env.example](.env.example) and can be overridden at runtime via `POST /api/v1/config` without restarting the server.

### LLM Provider Auto-Detection

The factory auto-detects the provider from the model name:

| Pattern | Provider |
|---------|----------|
| `provider/model` (contains `/`) | OpenRouter |
| `gpt-*`, `o1-*`, `o2-*`, `o3-*`, `o4-*`, `text-*`, `gpt-5*` | OpenAI direct |
| `claude-*` | Anthropic direct |
| `ollama/*` | Ollama |
| `google/*`, `vertex_ai/*` | Google Gemini/Vertex AI |
| Other | LM Studio local |

---

## Usage

### REST API (Recommended)

The primary interface is the FastAPI REST API:

```bash
# Start the server
python -m scripts.serve_api              # Default: http://127.0.0.1:8000
python -m scripts.serve_api --reload     # Auto-reload for development
```

**API Endpoints Summary:**

| Group | Endpoints | Description |
|-------|-----------|-------------|
| **Health** | `GET /health` | Liveness probe (no auth) |
| **Config** | `GET/POST /api/v1/config` | View/override runtime settings |
| **Build** | `POST /demo/build`, `/build/upload` | Build KG from docs + DDL |
| **Query** | `POST /demo/query` | Synchronous Q&A against loaded KG |
| **Pipeline** | `POST /demo/pipeline`, `/pipeline/upload` | Full E2E: build + query |
| **Graph** | `GET /demo/graph/stats`, `/graph/data` | Live Neo4j statistics and export |
| **Snapshots** | CRUD `/demo/kg/snapshots` | Save/load/manage KG snapshots |
| **Conversations** | CRUD `/demo/conversations` | Persist chat history |
| **Ablation** | `POST /ablation/run/preset`, `/run/custom` | Launch ablation studies |
| **Results** | `GET /ablation/bundle/...`, `/evaluate/...` | Download bundles, AI Judge payloads |

All `/api/v1/*` endpoints require `X-API-Key` header when `API_KEY` is set.
Swagger UI at `http://localhost:8000/docs`.

### CLI Scripts

```bash
# Run the full pipeline (build + evaluate) on one or more datasets
pipeline-run --best --dataset 01 --auto-neo4j

# Run ablation study
pipeline-run --study AB-03 --all-datasets

# Run AI Judge evaluation on completed bundles
ai-judge --all

# Neo4j database management
python -m scripts.neo4j_lifecycle --help
```

### Python API (Programmatic)

```python
from src.graph.builder_graph import run_builder

run_builder(
    raw_documents=["path/to/docs.pdf"],
    ddl_paths=["path/to/schema.sql"],
    production=False,
    clear_graph=True,
)
```

```python
from src.generation.query_graph import run_query

result = run_query("Which table stores customer data?")
print(result["final_answer"])
```

---

## Project Structure

```ascii
src/
  config/           Settings, LLM factory, logging, provider detection, tracing, observability
  models/           Pydantic v2 schemas + LangGraph state TypedDicts
  prompts/          Prompt templates + few-shot loaders
  ingestion/        PDF loader, DDL parser (sqlglot), schema enricher
  extraction/       Triplet extractor (SLM JSON mode) + heuristic fallback
  resolution/       Entity resolution (K-NN blocking + LLM judge)
  mapping/          RAG mapper, Actor-Critic validator, HITL interrupt
  graph/            Neo4j client, Cypher gen/heal/build, Builder Graph DAG
  retrieval/        BGE-M3 embeddings, BM25, hybrid retriever, cross-encoder reranker
  generation/       Answer generator, hallucination grader, Query Graph DAG
  evaluation/       RAGAS runner, custom metrics, ablation runner, bundle writer
  api/              FastAPI application (demo + ablation endpoints)
  utils/            JSON/text/query utilities

scripts/            Pipeline runners, API server, AI Judge, ablation tools, Neo4j lifecycle
tests/
  unit/             Unit tests (no external services)
  integration/      Integration tests (Neo4j required)
  evaluation/       Evaluation tests (ablation, gold standard loader, RAGAS)
  fixtures/         7 synthetic datasets with gold standard QA pairs
docs/
  draft/            Architecture specs, requirements, prompts, ADRs, ablation plan, datasets, test plan
  changelogs/       Version changelogs (v1.0.0 → v1.2.0)
  audits/           Security audit reports
  AI_JUDGE_PROMPT.md  AI Judge system prompt
  RUNNING_SERVICES.md  Setup guide
```

---

## Evaluation

### Evaluation Results (AB-BEST)

Best configuration evaluated across 7 datasets (111 tables, 210 questions), scored by AI Judge (`gpt-5.4-nano-2026-03-17`):

| Dataset | Tables | Questions | Grounded | Score |
|---------|:------:|:---------:|:--------:|:-----:|
| DS01 E-commerce | 7 | 15 | 15/15 | **5.00** |
| DS02 Finance | 8 | 25 | 25/25 | **5.00** |
| DS03 Healthcare | 10 | 30 | 30/30 | **4.70** |
| DS04 Manufacturing | 13 | 40 | 40/40 | **4.75** |
| DS05 Edge: Incomplete | 5 | 20 | 20/20 | **4.30** |
| DS06 Edge: Legacy | 10 | 25 | 25/25 | **5.00** |
| DS07 Stress (58 tables) | 58 | 55 | 55/55 | **4.35** |

**210/210 answers grounded (100%), zero hallucinations.** Average score **4.73/5**.

### Ablation Campaign

21 ablation studies + AB-BEST variant (K20), evaluated by AI Judge on a 1–5 scale:

| Study | Description | Score | Delta vs AB-00 |
|-------|-------------|:-----:|:--------------:|
| AB-04 | Reranker top_k=5 (AB-BEST) | **4.90** | +0.65 |
| AB-05 | Reranker top_k=20 | 4.90 | +0.65 |
| AB-00 | Baseline (full pipeline) | 4.25 | -- |
| AB-01 | Vector-only retrieval (worst) | 3.40 | -0.85 |

Key findings:
1. **Hybrid retrieval is non-negotiable** — Vector-only scores 3.40 (-0.85 vs baseline)
2. **Reranker top_k is the only discriminating parameter** — AB-04/AB-05 both 4.90
3. **top_k=5 is the efficient optimum** — Same quality as top_k=20 with 4× fewer cross-encoder calls
4. **K5 validated across all 7 datasets** — K5 avg 4.73 vs K20 avg 4.53 (K5 wins 6/7)
5. **Schema enrichment and Actor-Critic are critical safety nets** — Disabling either drops GT coverage ≥33 pp

Full results in [docs/ablation/RESULTS.md](docs/ablation/RESULTS.md).

---

## Documentation

| Document | Description |
|----------|-------------|
| [docs/RUNNING_SERVICES.md](docs/RUNNING_SERVICES.md) | Service setup guide (Neo4j, environment, API server) |
| [docs/ablation/RESULTS.md](docs/ablation/RESULTS.md) | Full ablation results, K5 vs K20 comparison, DS05 deep dive |
| [docs/AI_JUDGE_PROMPT.md](docs/AI_JUDGE_PROMPT.md) | AI Judge system prompt for evaluation |
| [docs/draft/REQUIREMENTS.md](docs/draft/REQUIREMENTS.md) | Functional and non-functional requirements by epic |
| [docs/draft/SPECS.md](docs/draft/SPECS.md) | Architecture specifications, state schemas, node specs |
| [docs/draft/PROMPTS.md](docs/draft/PROMPTS.md) | Complete prompt template catalogue |
| [docs/draft/ADR.md](docs/draft/ADR.md) | Architecture Decision Records (15 ADRs) |
| [docs/draft/ABLATION.md](docs/draft/ABLATION.md) | Ablation study plan and methodology |
| [docs/draft/DATASET.md](docs/draft/DATASET.md) | Dataset specifications (inputs, few-shot, gold standard) |
| [docs/draft/TEST_PLAN.md](docs/draft/TEST_PLAN.md) | Test strategy and test case catalogue |
| [docs/changelogs/](docs/changelogs/) | Version changelogs (v1.0.0 → v1.4.0) |
| [docs/audits/](docs/audits/) | Security audit reports |
| [docs/study-guide/](docs/study-guide/) | Module-by-module study guide (15 chapters) |

---

## License

MIT (c) 2026 Marc'Antonio Lopez. See [LICENSE](LICENSE).