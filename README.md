# Multi-Agent Framework for Semantic Discovery & GraphRAG

> A LangGraph-orchestrated multi-agent pipeline for automated **Data Governance**. Bridges the semantic gap between unstructured business documentation (PDF/TXT) and relational database schemas (DDL/SQL) by autonomously constructing a Knowledge Graph on Neo4j.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Development](#development)
- [Smoke Test Results](#smoke-test-results)

---

## Overview

This framework solves the core challenge of Data Governance: automatically connecting *what the business means* (expressed in free-text documents) with *what the database stores* (expressed in DDL schemas). It does so by running two coordinated LangGraph pipelines that together construct a queryable Knowledge Graph and answer natural-language questions against it.

---

## Architecture

### Two-Graph Pipeline

#### 1. Builder Graph (`src/graph/builder_graph.py`)

Responsible for ontology construction from raw documents and database schemas:

| Stage | Component | Description |
|-------|-----------|-------------|
| Ingestion | `pdf_loader`, `ddl_parser` | Loads PDF/TXT docs and parses DDL schemas |
| Triplet Extraction | `triplet_extractor` | Extracts `(subject, predicate, object)` triplets via LLM (JSON mode) |
| Entity Resolution | `blocking` + `llm_judge` | K-NN blocking groups candidates; LLM judge decides merge/separate |
| Schema Mapping | `rag_mapper` + `validator` | RAG-augmented mapping with Actor-Critic validation and optional HITL |
| Graph Construction | `cypher_generator` + `cypher_healer` | Generates Cypher, validates via EXPLAIN dry-run, auto-heals syntax errors |
| Upsert & FK Edges | `cypher_builder`, `neo4j_client` | Idempotent MERGE upserts + `REFERENCES` edges between `PhysicalTable` nodes |

#### 2. Query Graph (`src/generation/query_graph.py`)

Responsible for answering natural-language questions against the Knowledge Graph:

| Stage | Component | Description |
|-------|-----------|-------------|
| Retrieval | `hybrid_retriever` | Dense (BGE-M3) + BM25 + Graph traversal, fused via RRF |
| Reranking | `reranker` | Cross-encoder reranking with `bge-reranker-large` |
| Generation | `answer_generator` | LLM answer generation with critique injection |
| Grading | `hallucination_grader` | Self-RAG grader; emits `pass \| regenerate`; forces `pass` after max retries |

---

## Requirements

- **Python** 3.12+
- **Neo4j** 5.x

```bash
# Start Neo4j with Docker
docker run -d --name neo4j-thesis \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/password \
  neo4j:5
```

- **Cloud LLM access** (optional): `OPENROUTER_API_KEY` or `OPENAI_API_KEY` in `.env`
- **Local LLM** (optional): [LM Studio](https://lmstudio.ai/) running at `http://localhost:1234/v1`

---

## Installation

```bash
# Clone and enter the repo
git clone <repo-url>
cd thesis

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate

# Install with development dependencies
pip install -e ".[dev]"
```

---

## Configuration

The application uses a **two-tier configuration system**:

1. **`src/config/config.py`** — Non-sensitive defaults (Python dataclass). All defaults are visible in code and can be overridden via environment variables.
2. **`.env`** — Sensitive values only.

### Environment Variables

Create a `.env` file in the project root:

```dotenv
# Neo4j
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password

# Cloud LLM providers (set whichever you use)
OPENROUTER_API_KEY=sk-or-...
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Local LLM (LM Studio)
LMSTUDIO_BASE_URL=http://localhost:1234/v1

# Model selection
LLM_MODEL_REASONING=openai/gpt-oss-120b
LLM_MODEL_EXTRACTION=local-model
```

### LLM Provider Auto-Detection

The factory (`llm_factory.detect_provider`) selects the provider automatically from the model name:

| Model name pattern | Provider |
|--------------------|----------|
| Contains `/` (e.g. `openai/gpt-oss-120b`, `meta-llama/llama-3.3-70b-instruct:free`) | **OpenRouter** |
| `gpt-*`, `o1-*`, `o3-*` (no slash) | **OpenAI** direct |
| `claude-*` (no slash) | **Anthropic** direct |
| Anything else (e.g. `local-model`) | **LM Studio** local |

---

## Usage

### Accessing Configuration in Code

```python
from src.config.settings import get_settings

settings = get_settings()
model = settings.llm_model_reasoning
threshold = settings.confidence_threshold
```

### Running the Interactive Demo

```bash
jupyter notebook notebooks/00_interactive_demo.ipynb
```

### Running Evaluation

```bash
ragas-eval   # CLI entry point for RAGAS evaluation
```

---

## Project Structure

```
src/
├── config/           # Settings, LLM factory, logging, LLM client
├── models/           # Pydantic schemas + LangGraph state TypedDicts
├── prompts/          # Prompt templates + few-shot loaders
├── ingestion/        # PDF loader, DDL parser, schema enricher
├── extraction/       # Triplet extractor (JSON mode)
├── resolution/       # Entity resolution (blocking + LLM judge)
├── mapping/          # RAG mapper, Actor-Critic validator, HITL
├── graph/            # Neo4j client, Cypher gen/heal/build, Builder Graph
├── retrieval/        # BGE-M3 embeddings, hybrid retriever, cross-encoder
├── generation/       # Answer generator, hallucination grader, Query Graph
└── evaluation/       # RAGAS runner, custom metrics, ablation runner

notebooks/
└── 00_interactive_demo.ipynb  # End-to-end interactive demonstration

tests/
├── unit/             # 313 tests — no external services required
└── integration/      # Neo4j required (testcontainers)
```

---

## Development

```bash
# Activate environment
source .venv/bin/activate

# Run unit tests
pytest tests/unit/ -v

# Run integration tests (requires Neo4j)
pytest tests/integration/ -v

# Lint
ruff check src/ tests/

# Auto-fix linting issues
ruff check --fix src/ tests/

# Format
ruff format src/ tests/

# Type check
mypy src/
```

---

## Smoke Test Results

End-to-end smoke test against a sample business glossary + two-table DDL schema:

| Metric | Result |
|--------|--------|
| Triplets extracted | 42 |
| Entities resolved | 38 |
| Tables mapped | 2 / 2 |
| Mapping confidence | Customer 95% · Sales Order 95% |
| Q&A queries answered | 3 / 3 (all with hallucination grading) |