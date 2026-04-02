# Multi-Agent Framework for Semantic Discovery & GraphRAG

**A LangGraph-orchestrated multi-agent system for automated Data Governance.**

This framework bridges the semantic gap between unstructured business documentation (PDF/TXT) and relational database schemas (DDL/SQL) by autonomously constructing a Knowledge Graph on Neo4j and answering natural-language queries against it.

Developed as a Master's thesis project at Politecnico di Torino, March 2026.

---

## Table of Contents

- [Abstract](#abstract)
- [Architecture](#architecture)
- [Key Features](#key-features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Evaluation](#evaluation)
- [Development](#development)
- [Documentation](#documentation)
- [License](#license)

---

## Abstract

Data Governance requires aligning business semantics (expressed in free-text glossaries, data dictionaries, and process descriptions) with the physical structures of relational databases. This alignment is traditionally performed manually by data stewards, a process that is error-prone, time-consuming, and does not scale.

This project proposes a **generative AI framework** that automates this alignment through two coordinated LangGraph pipelines:

1. **Builder Graph** -- Ingests business documents and DDL schemas, extracts semantic triplets, resolves entities, maps business concepts to physical tables, and upserts the resulting ontology into a Neo4j Knowledge Graph.

2. **Query Graph** -- Answers natural-language questions against the Knowledge Graph using hybrid retrieval (dense vector + BM25 + graph traversal), cross-encoder reranking, and hallucination-graded answer generation.

The system employs self-reflection loops (Actor-Critic validation, Cypher healing), a provider-agnostic multi-tier LLM factory, and a comprehensive ablation study framework (21 studies across 6 datasets) to quantify the marginal contribution of each architectural component.

---

## Architecture

### Two-Graph Pipeline

```
Business Docs (PDF/TXT)         DDL Schemas (SQL)
        |                              |
        v                              v
  +-----------+                 +-----------+
  |  Triplet  |                 | DDL Parse |
  | Extraction|                 |  + Schema |
  |  (SLM)   |                 | Enrichment|
  +-----------+                 +-----------+
        |                              |
        v                              |
  +-----------+                        |
  |  Entity   |                        |
  | Resolution|                        |
  | (K-NN +   |                        |
  |  LLM)     |                        |
  +-----------+                        |
        |                              |
        +----------+   +--------------+
                   v   v
            +----------------+
            |  RAG Mapping   |
            |  (Map-Reduce   |  <-- Actor-Critic Loop
            |   per table)   |
            +----------------+
                   |
                   v
            +----------------+
            | Cypher Gen +   |  <-- Cypher Healing Loop
            | Neo4j Upsert   |
            +----------------+
                   |
                   v
            +================+
            | NEO4J KNOWLEDGE|
            |     GRAPH      |
            +================+
                   |
                   v
            +----------------+
            | Hybrid         |
            | Retrieval +    |
            | Reranking +    |
            | Answer Gen +   |
            | Hallucination  |
            | Grading        |
            +----------------+
                   |
                   v
            Grounded Answer
```

### Builder Graph

| Stage | Module | Description |
|-------|--------|-------------|
| Ingestion | `ingestion/pdf_loader`, `ddl_parser` | Load PDF/TXT documents, parse DDL schemas via sqlglot |
| Schema Enrichment | `ingestion/schema_enricher` | LLM expands abbreviated identifiers (e.g. `TB_CST` to `Customer Table`) |
| Triplet Extraction | `extraction/triplet_extractor` | SLM extracts `(subject, predicate, object)` triplets in JSON mode |
| Entity Resolution | `resolution/blocking` + `llm_judge` | Two-stage: K-NN blocking with BGE-M3 embeddings, then LLM judge decides merge/separate |
| RAG Mapping | `mapping/rag_mapper` + `validator` | Map-Reduce RAG per table with Actor-Critic validation loop |
| HITL | `mapping/hitl` | LangGraph interrupt for low-confidence mappings |
| Graph Build | `graph/cypher_generator` + `cypher_healer` | LLM generates Cypher, EXPLAIN dry-run validates, auto-healing on syntax errors |
| Upsert | `graph/build_nodes` + `cypher_builder` | MERGE upserts + FK edge construction |

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
- **Self-reflection loops** -- Actor-Critic mapping validation with best-proposal tracking; Cypher healing with deterministic fallback builder.
- **Hybrid retrieval with RRF** -- Three retrieval channels merged without weight tuning, followed by cross-encoder reranking.
- **Comprehensive ablation framework** -- 21 studies across 6 synthetic datasets with automated AI Judge evaluation.
- **REST API** -- FastAPI endpoints for demo pipeline execution and ablation study management.
- **Debug tracing** -- Optional per-query trace output for analysis and debugging.

---

## Requirements

- **Python** 3.11+
- **Neo4j** 5.x

```bash
# Start Neo4j with Docker
docker run -d --name neo4j-thesis \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/your_password_here \
  neo4j:5
```

**LLM access** (at least one):
- Cloud provider API key (`OPENROUTER_API_KEY`, `OPENAI_API_KEY`, or `ANTHROPIC_API_KEY`)
- Local LLM server (LM Studio at `http://localhost:1234/v1`)

---

## Installation

```bash
git clone <repo-url>
cd thesis

python -m venv .venv
source .venv/bin/activate

pip install -e ".[dev]"
```

---

## Configuration

The application uses a two-tier configuration system:

1. **`src/config/config.py`** -- Non-sensitive defaults (dataclass). All defaults are visible in code and overridable via environment variables.
2. **`.env`** -- Sensitive values only (API keys, passwords).

### Environment Variables

Create a `.env` file in the project root:

```dotenv
# Neo4j
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password_here

# Cloud LLM providers (set whichever you use)
OPENROUTER_API_KEY=sk-or-...
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Local LLM (LM Studio)
LMSTUDIO_BASE_URL=http://localhost:1234/v1

# Model selection (examples)
LLM_MODEL_REASONING=gpt-5.4
LLM_MODEL_EXTRACTION=gpt-5.4-nano
LLM_MODEL_MIDTIER=gpt-5.4-mini
```

### LLM Provider Auto-Detection

The factory auto-detects the provider from the model name:

| Pattern | Provider |
|---------|----------|
| `provider/model` (contains `/`) | OpenRouter |
| `gpt-*`, `o1-*`, `o3-*`, `o4-*`, `gpt-5*` | OpenAI direct |
| `claude-*` | Anthropic direct |
| `ollama/*` | Ollama |
| `google/*`, `vertex_ai/*` | Google Gemini/Vertex AI |
| Other | LM Studio local |

---

## Usage

### Running the Builder Pipeline

```bash
python -m scripts.pipeline_run --help
```

### Running Queries

```bash
python -m scripts.pipeline_run --mode query --question "Which table stores customer data?"
```

### REST API

```bash
python -m scripts.serve_api              # Default: http://127.0.0.1:8000
python -m scripts.serve_api --reload     # Auto-reload on code changes
```

Swagger UI at `http://127.0.0.1:8000/docs`.

### Interactive Demo

```bash
jupyter notebook notebooks/00_interactive_demo.ipynb
```

### Neo4j Management

```bash
python -m scripts.neo4j_lifecycle --help  # Clear database, setup schema
```

### Ablation Studies

```bash
# Run a single ablation study
python -m scripts.run_ablation_full --study AB-10 --dataset DS01

# Run full campaign (21 studies x 6 datasets)
python -m scripts.run_ablation_full --all
```

---

## Project Structure

```
src/
  config/           Settings, LLM factory, logging, provider detection, tracing
  models/           Pydantic v2 schemas + LangGraph state TypedDicts
  prompts/          Prompt templates + few-shot loaders
  ingestion/        PDF loader, DDL parser, schema enricher
  extraction/       Triplet extractor (SLM, JSON mode) + heuristic fallback
  resolution/       Entity resolution (K-NN blocking + LLM judge)
  mapping/          RAG mapper, Actor-Critic validator, HITL interrupt
  graph/            Neo4j client, Cypher gen/heal/build, Builder Graph DAG
  retrieval/        BGE-M3 embeddings, BM25, hybrid retriever, cross-encoder
  generation/       Answer generator, hallucination grader, Query Graph DAG
  evaluation/       RAGAS runner, custom metrics, ablation runner
  api/              FastAPI application (demo + ablation endpoints)
  utils/            JSON/text utilities

scripts/            Pipeline runners, ablation tools, Neo4j lifecycle
notebooks/          Interactive demo, ablation analysis
tests/
  unit/             Unit tests (no external services)
  integration/      Integration tests (Neo4j required)
  fixtures/         Sample docs, DDL, mock responses, gold standard
docs/
  draft/            Architecture specs, requirements, prompts, ADRs, ablation plan
  implementation/   Step-by-step implementation guides
  completed/        Session reports, cleanup audits
```

---

## Evaluation

### Ablation Campaign

21 ablation studies across 6 synthetic datasets (126 total runs), evaluated by an AI Judge (GPT-5.4-mini) on a 1.0--5.0 scale:

| Study | Description | Mean Score | Delta |
|-------|-------------|-----------|-------|
| AB-00 | Baseline (full pipeline) | 4.15 | -- |
| AB-10 | Extraction tokens=16384 (best) | 4.46 | +0.31 |
| AB-01 | Vector-only retrieval (worst) | 2.49 | -1.66 |
| AB-20 | Hallucination grader OFF | 3.35 | -0.80 |
| AB-19 | Cypher healing OFF | 3.63 | -0.52 |
| AB-03 | Reranker OFF | 3.65 | -0.50 |

Key findings:
- Hybrid retrieval is the single most critical component (-1.66 when reduced to vector-only)
- The hallucination grader provides substantial quality improvement (-0.80 when disabled)
- Larger extraction token budgets improve triplet richness (+0.31)

Full results in `docs/draft/ABLATION.md` and `notebooks/ablation/ablation_results/ABLATION_ANALYSIS_COMPLETE.md`.

---

## Development

```bash
source .venv/bin/activate

# Testing
pytest tests/unit/ -v                    # Unit tests
pytest tests/integration/ -v             # Integration tests (Neo4j required)
pytest -m "not integration" -v           # All except integration

# Code quality
ruff check src/ tests/                   # Lint
ruff check --fix src/ tests/             # Auto-fix
ruff format src/ tests/                  # Format
mypy src/                                # Type check
```

---

## Documentation

| Document | Description |
|----------|-------------|
| `docs/draft/SPECS.md` | Architecture specifications, state schemas, node specs |
| `docs/draft/REQUIREMENTS.md` | Functional and non-functional requirements by epic |
| `docs/draft/PROMPTS.md` | Complete prompt template catalogue |
| `docs/draft/ADR.md` | Architecture Decision Records (15 ADRs) |
| `docs/draft/ABLATION.md` | Ablation study plan and results |
| `docs/draft/DATASET.md` | Dataset specifications (inputs, few-shot, gold standard) |
| `docs/draft/TEST_PLAN.md` | Test strategy and test case catalogue |
| `docs/implementation/00-overview.md` | Implementation guides index |
| `CLAUDE.md` | Development conventions and codebase guide |

---

## License

See [LICENSE](LICENSE).
