# Thesis Project: Multi-Agent Framework for Semantic Discovery & GraphRAG

> **Status:** Complete — March 2026
> **Author:** Marc'Antonio Lopez
> **Scope:** Generative AI system for automated Data Governance via LangGraph-orchestrated multi-agent architecture.

---

## Table of Contents

1. [Abstract](#1-abstract)
2. [Architectural Vision](#2-architectural-vision)
3. [Tech Stack](#3-tech-stack)
4. [LangGraph State Schemas](#4-langgraph-state-schemas)
5. [Flow 1 — Builder Graph (Ontology Construction)](#5-flow-1--builder-graph-ontology-construction)
6. [Flow 2 — Query Graph (Advanced Agentic RAG)](#6-flow-2--query-graph-advanced-agentic-rag)
7. [Prompting Strategies & Context Management](#7-prompting-strategies--context-management)
8. [Self-Reflection Loops](#8-self-reflection-loops)
9. [Evaluation Framework](#9-evaluation-framework)
10. [REST API](#10-rest-api)
11. [Known Limits & Future Work](#11-known-limits--future-work)

---

## 1. Abstract

This thesis designs and implements a **Generative AI framework for Data Governance automation**. The system bridges the **semantic gap** between unstructured business documentation (PDF) and relational database schemas (DDL/SQL) by autonomously constructing a **Knowledge Graph on Neo4j**.

**Core innovations:**

| Innovation | Description |
|---|---|
| **Two-Graph Architecture** | Builder Graph for ontology construction + Query Graph for agentic RAG |
| **Multi-Tier LLM Factory** | 5-tier model routing: nano, extraction, midtier, generation, reasoning |
| **Self-Reflection Loops** | Actor-Critic validation + Cypher Healing (error injection to auto-fix) |
| **Advanced GraphRAG** | Hybrid retrieval (Vector + BM25 + Graph) with cross-encoder reranking |
| **Provider-Agnostic Design** | `LLMProtocol` structural type — works with OpenRouter, OpenAI, Anthropic, Ollama, LM Studio |

**Problem solved:** Feeding an entire SQL schema to a monolithic LLM causes context window overload and hallucinations. This system decomposes the reasoning task into a **cognitive graph pipeline** with isolated, specialised nodes.

---

## 2. Architectural Vision

### 2.1 Paradigm Shift

```
Zero-Shot Monolithic Prompting  →  Agentic Workflow (LangGraph DAG)
Single LLM call on full schema  →  Specialised nodes, isolated context windows
No validation                   →  Self-reflection loops (Actor-Critic + Cypher Healing)
Static retrieval                →  Hybrid GraphRAG (Vector + BM25 + Graph Traversal)
Single LLM provider             →  Provider-agnostic multi-tier factory
```

### 2.2 High-Level System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        INPUTS                                       │
│  PDF Documents (business glossaries, data dictionaries)             │
│  DDL Schemas (SQL CREATE TABLE statements)                          │
└──────────┬──────────────────────────────────────┬───────────────────┘
           │                                      │
           ▼                                      ▼
┌──────────────────────┐              ┌───────────────────────┐
│  BUILDER GRAPH       │              │  DDL PIPELINE         │
│  Extract Triplets    │              │  Parse DDL            │
│  Entity Resolution   │              │  Schema Enrichment    │
│  (blocking + judge)  │              │  (LLM acronym expand) │
└──────────┬───────────┘              └───────────┬───────────┘
           │                                      │
           └──────────────┬───────────────────────┘
                          ▼
              ┌───────────────────────┐
              │  RAG Mapping          │
              │  (Map-Reduce per      │
              │   table)              │
              └───────────┬───────────┘
                          ▼
              ┌───────────────────────┐
              │  Validate (Pydantic   │    ◄── Actor-Critic Loop
              │   + LLM Critic)       │
              └───────────┬───────────┘
                          ▼
              ┌───────────────────────┐
              │  HITL Breakpoint      │    ◄── confidence < threshold
              └───────────┬───────────┘
                          ▼
              ┌───────────────────────┐
              │  Generate Cypher      │    ◄── Cypher Healing Loop
              │  + Build Graph (Neo4j)│
              └───────────┬───────────┘
                          ▼
              ┌───────────────────────┐
              │  NEO4J KNOWLEDGE      │
              │  GRAPH                │
              │  BusinessConcept      │
              │  PhysicalTable        │
              │  MAPPED_TO edges      │
              │  REFERENCES edges     │
              └───────────┬───────────┘
                          ▼
              ┌───────────────────────┐
              │  QUERY GRAPH          │
              │  Hybrid Retrieval     │
              │  Cross-Encoder Rerank │
              │  Answer Generation    │
              │  Hallucination Grader │
              └───────────┬───────────┘
                          ▼
              ┌───────────────────────┐
              │  Final Grounded       │
              │  Answer               │
              └───────────────────────┘
```

### 2.3 Neo4j Ontology Meta-Model

```
(:BusinessConcept {name, definition, source_doc, synonyms, confidence_score, provenance_text})
(:PhysicalTable {table_name, schema_name, column_names, column_types, ddl_source})

(:BusinessConcept)-[:MAPPED_TO {confidence, validated_by, created_at}]->(:PhysicalTable)
(:BusinessConcept)-[:RELATED_TO]->(:BusinessConcept)
(:PhysicalTable)-[:REFERENCES {fk_column, ref_column}]->(:PhysicalTable)
```

**Key Cypher patterns (MERGE upsert strategy):**

```cypher
-- Upsert a BusinessConcept
MERGE (bc:BusinessConcept {name: $name})
ON CREATE SET bc.definition = $definition, bc.provenance_text = $provenance
ON MATCH SET bc.confidence_score = $confidence

-- Upsert a PhysicalTable
MERGE (pt:PhysicalTable {table_name: $table_name})
ON CREATE SET pt.schema_name = $schema, pt.column_names = $columns

-- Create semantic alignment
MATCH (bc:BusinessConcept {name: $concept})
MATCH (pt:PhysicalTable {table_name: $table})
MERGE (bc)-[:MAPPED_TO {confidence: $score, validated_by: $validator}]->(pt)

-- FK edge upsert (cypher_builder.py)
MERGE (child:PhysicalTable {table_name: $child_table})
MERGE (parent:PhysicalTable {table_name: $parent_table})
MERGE (child)-[:REFERENCES {fk_column: $fk_col, ref_column: $ref_col}]->(parent)
```

---

## 3. Tech Stack

### 3.1 Component Overview

| Layer | Component | Role |
|---|---|---|
| **Orchestration** | LangGraph | DAG state machine, conditional routing, checkpointing |
| **Chain Management** | LangChain | Prompt templates, chain composition |
| **LLM Factory** | `src/config/llm_factory.py` | 5-tier model routing, provider auto-detection |
| **Dense Embeddings** | BGE-M3 (BAAI) | 1024-dim multilingual semantic embeddings |
| **Reranking** | bge-reranker-v2-m3 (BAAI) | Cross-encoder scoring (query x chunk) |
| **Graph + Vector DB** | Neo4j 5.x | Graph topology + vector index + fulltext BM25 |
| **Validation** | Pydantic v2 | Schema enforcement on LLM outputs |
| **Evaluation** | RAGAS + AI Judge | RAG quality metrics + LLM-as-a-judge |
| **API** | FastAPI + uvicorn | REST endpoints for demo and ablation |

### 3.2 LLM Factory Tiers

The LLM factory (`src/config/llm_factory.py`) provides five tiers of model access, each optimised for a specific task class:

| Tier | Function | Default Model | Role | Temperature |
|---|---|---|---|---|
| **Nano** | `get_lightweight_llm()` | gpt-5.4-nano | ER judge, schema enrichment | 0.0 |
| **Extraction** | `get_extraction_llm()` | gpt-5.4-nano | Triplet extraction (JSON Mode) | 0.0 |
| **Midtier** | `get_midtier_llm()` | gpt-5.4-mini | RAG mapping, Actor-Critic, hallucination grading | 0.0 |
| **Generation** | `get_generation_llm()` | (same as reasoning) | Answer generation | 0.3 |
| **Reasoning** | `get_reasoning_llm()` | gpt-5.4 | Cypher generation, complex reasoning | 0.0 |

**Provider auto-detection** (`src/config/provider_detection.py`):
- `"provider/model"` (contains `/`) → OpenRouter
- `"gpt-*"`, `"o1-*"`, `"o3-*"`, `"o4-*"`, `"gpt-5*"` → OpenAI direct
- `"claude-*"` → Anthropic direct
- `"ollama/*"` → Ollama
- `"google/*"`, `"vertex_ai/*"` → Google Gemini/Vertex AI
- Anything else → LM Studio local

All node functions type-annotate LLMs as `llm: LLMProtocol` (structural type) for provider agnosticism.

### 3.3 Embeddings & Reranker (GPU Auto-Detection)

- **BGE-M3** (`get_embeddings()`): auto-detects GPU via `torch.cuda.is_available()` — uses `devices=["cuda:0"]` + `use_fp16=True` if available, else CPU
- **bge-reranker-v2-m3** (`get_reranker()`): same auto-detection — uses `device="cuda:0"` + `use_fp16=True` if available, else CPU

---

## 4. LangGraph State Schemas

Defined in `src/models/state.py` as `TypedDict` with `total=False` (all fields optional).

### 4.1 BuilderState

```python
class BuilderState(TypedDict, total=False):
    # Entry-point inputs
    ddl_paths: list[str]
    source_doc: str
    use_lazy_extraction: bool

    # Ingestion
    documents: list[Document]
    chunks: list[Chunk]

    # Extraction + Entity Resolution
    triplets: list[Triplet]
    entities: list[Entity]

    # Schema parsing
    tables: list[TableSchema]
    enriched_tables: list[EnrichedTableSchema]

    # Mapping (queue-based, one table at a time)
    pending_tables: list[EnrichedTableSchema]
    current_table: EnrichedTableSchema | None
    current_entities: list[Entity]
    mapping_proposal: MappingProposal | None
    best_proposal: MappingProposal | None          # Actor-Critic best-seen tracking
    reflection_prompt: str | None
    reflection_attempts: int

    # Cypher
    current_cypher: str | None
    healing_attempts: int
    cypher_failed: bool

    # Control
    hitl_flag: bool
    skip_hitl: bool
    failed_mappings: list[str]
    ingestion_errors: list[str]
    completed_tables: list[str]

    # Debug tracing
    trace_enabled: bool
    builder_trace: Any                              # BuilderTrace | None at runtime
    trace_output_dir: str
```

### 4.2 QueryState

```python
class QueryState(TypedDict, total=False):
    user_query: str

    # Retrieval
    retrieved_chunks: list[RetrievedChunk]
    reranked_chunks: list[RetrievedChunk]
    generation_chunks: list[RetrievedChunk]

    # Retrieval quality assessment
    retrieval_quality_score: float
    retrieval_chunk_count: int
    retrieval_filtered_by_threshold: bool
    context_sufficiency: str                        # "adequate" | "sparse" | "insufficient"
    retrieval_gate_decision: str

    # Generation
    current_answer: str
    last_critique: str | None
    grader_decision: GraderDecision | None
    final_answer: str
    sources: list[str]
    retrieved_contexts: list[str]

    # Grader state
    grader_consistency_valid: bool
    grader_rejection_count: int
    iteration_count: int

    # Debug tracing
    query_trace_enabled: bool
    query_trace: Any                                # QueryTrace | None at runtime
    query_index: int
    builder_trace_id: str
```

---

## 5. Flow 1 — Builder Graph (Ontology Construction)

### 5.1 Node Specifications

| Node | Module | Model Tier | T | Input | Output | Key Pattern |
|---|---|---|---|---|---|---|
| `_node_ingest_pdf` | `ingestion/pdf_loader.py` | — | — | PDF paths | documents, chunks | RecursiveCharacterTextSplitter |
| `_node_extract_triplets` | `extraction/triplet_extractor.py` | Extraction | 0.0 | chunks | triplets | JSON Mode + self-reflection |
| `_node_heuristic_extract` | `extraction/heuristic_extractor.py` | — | — | chunks | triplets | spaCy NLP fallback |
| `_node_resolve_entities` | `resolution/entity_resolver.py` | Nano | 0.0 | triplets | entities | Two-stage: K-NN blocking + LLM judge |
| `_node_parse_ddl` | `ingestion/ddl_parser.py` | — | — | DDL paths | tables | sqlglot deterministic parsing |
| `_node_enrich_schema` | `ingestion/schema_enricher.py` | Nano | 0.0 | tables | enriched_tables | Zero-Shot acronym expansion |
| `_node_init_mapping_queue` | `graph/build_nodes.py` | — | — | enriched_tables | pending_tables | Queue initialisation |
| `_node_pop_next_table` | `graph/build_nodes.py` | — | — | pending_tables | current_table | Pop from queue |
| `_node_rag_mapping` | `mapping/rag_mapper.py` | Midtier | 0.0 | current_table + entities | mapping_proposal | Map-Reduce per table + few-shot |
| `_node_validate_mapping` | `mapping/validator.py` | Midtier | 0.0 | mapping_proposal | approved/rejected | Pydantic + Actor-Critic |
| `_node_hitl_review` | `mapping/hitl.py` | — | — | proposal | approved mapping | LangGraph interrupt() |
| `_node_generate_cypher` | `graph/cypher_generator.py` | Reasoning | 0.0 | mapping + table | current_cypher | LLM + few-shot |
| `_node_test_cypher` | `graph/cypher_healer.py` | — | — | current_cypher | pass/fail | EXPLAIN dry-run on Neo4j |
| `_node_fix_cypher` | `graph/cypher_healer.py` | Reasoning | 0.0 | cypher + error | corrected_cypher | Error injection reflection |
| `_node_build_graph` | `graph/build_nodes.py` | — | — | cypher | Neo4j commit | MERGE upsert + FK edges |

### 5.2 Self-Reflection Details

**Actor-Critic Loop:**
1. LLM Actor generates `MappingProposal`
2. Pydantic validates structure
3. LLM Critic reviews semantic correctness
4. If rejected → inject critique into `REFLECTION_TEMPLATE` → retry
5. After `max_reflection_attempts` → use `best_proposal` (highest confidence seen across all retries)

**Cypher Healing Loop:**
1. LLM generates Cypher from mapping
2. `EXPLAIN` dry-run against Neo4j
3. If `CypherSyntaxError` → inject error into `CYPHER_FIX_USER` → retry
4. After `max_cypher_healing_attempts` → fall back to `cypher_builder.build_upsert_cypher()` (deterministic, parameterless)

### 5.3 Incremental Graph Update (Upsert Strategy)

The graph is **never rebuilt from scratch**. Every write uses `MERGE` (upsert semantics). The LLM only processes the **delta** (new/changed documents or tables), not the full corpus.

---

## 6. Flow 2 — Query Graph (Advanced Agentic RAG)

### 6.1 Node Specifications

| Node | Module | Model Tier | T | Input | Output |
|---|---|---|---|---|---|
| `_node_hybrid_retrieval` | `retrieval/hybrid_retriever.py` | — | — | user_query | retrieved_chunks |
| `_node_retrieval_quality_gate` | `generation/nodes/retrieval_nodes.py` | — | — | retrieved_chunks | gate_decision |
| `_node_rerank` | `retrieval/reranker.py` | — | — | retrieved_chunks | reranked_chunks |
| `_node_context_distill` | `generation/context_distiller.py` | — | — | reranked_chunks | generation_chunks |
| `_node_lazy_expand` | `generation/lazy_expander.py` | — | — | generation_chunks | expanded_chunks |
| `_node_generate_answer` | `generation/answer_generator.py` | Generation | 0.3 | chunks + query | current_answer |
| `_node_grade_answer` | `generation/hallucination_grader.py` | Midtier | 0.0 | answer + context | grader_decision |
| `_node_grader_consistency` | `generation/nodes/generation_nodes.py` | — | — | grader_decision | consistency check |

### 6.2 Hybrid Retrieval — Mechanism Breakdown

| Retrieval Method | What It Captures | Failure Mode Addressed |
|---|---|---|
| **Dense Vector** (BGE-M3) | Semantic similarity, paraphrases | Lexical gap (synonym mismatch) |
| **BM25 Keyword** | Exact string matches (table IDs, codes) | Embedding dilution on rare tokens |
| **Graph Traversal** | Topological neighbours, related concepts | Isolated chunk missing relational context |

All three results are merged via **Reciprocal Rank Fusion (RRF)** — no weight tuning required. The merged pool is then fed to the cross-encoder reranker which jointly scores each `(query, chunk)` pair. Only **Top-K** chunks pass to generation.

### 6.3 Context Sufficiency Assessment

The retrieval quality gate evaluates retrieved chunks and sets `context_sufficiency` to one of three levels:

| Level | Description | System Prompt Used |
|---|---|---|
| `adequate` | Strong relevant context | `ANSWER_SYSTEM_ADEQUATE` |
| `sparse` | Partial but potentially useful evidence | `ANSWER_SYSTEM_SPARSE` |
| `insufficient` | Minimal or no relevant context | `ANSWER_SYSTEM_INSUFFICIENT` |

The answer generator selects the appropriate system prompt based on context sufficiency, with each variant calibrating the LLM's behaviour to the available evidence level.

### 6.4 Hallucination Grader — Critique Protocol

The grader emits a structured JSON with `grounded`, `critique`, and `action` fields. Actions drive LangGraph routing:

- `"pass"` → final output (answer is fully grounded)
- `"regenerate"` → back to answer generation with critique injected

After `max_hallucination_retries`, the grader forces `action="pass"` (accepts current answer).

---

## 7. Prompting Strategies & Context Management

### 7.1 Per-Node Prompt Configuration

| Node | System Prompt Constant | Temperature |
|---|---|---|
| `_node_extract_triplets` | `EXTRACTION_SYSTEM` | 0.0 |
| `_node_resolve_entities` (LLM judge) | `ER_JUDGE_SYSTEM` | 0.0 |
| `_node_enrich_schema` | `ENRICHMENT_SYSTEM` | 0.0 |
| `_node_rag_mapping` | `MAPPING_SYSTEM` | 0.0 |
| `_node_validate_mapping` (critic) | `CRITIC_SYSTEM` | 0.0 |
| All reflection retries | `REFLECTION_TEMPLATE` | inherits |
| `_node_generate_cypher` | `CYPHER_SYSTEM` | 0.0 |
| `_node_fix_cypher` | `CYPHER_SYSTEM` + `CYPHER_FIX_USER` | 0.0 |
| `_node_generate_answer` | `ANSWER_SYSTEM_ADEQUATE/SPARSE/INSUFFICIENT` | 0.3 |
| `_node_generate_answer` (retry) | `ANSWER_SYSTEM` + `ANSWER_WITH_CRITIQUE_USER` | 0.3 |
| `_node_grade_answer` | `GRADER_SYSTEM` | 0.0 |

All prompts are defined in `src/prompts/templates.py`. See [PROMPTS.md](./PROMPTS.md) for full template catalogue.

### 7.2 Temperature Strategy

$$
T_{extraction} = T_{mapping} = T_{enrichment} = T_{grading} = 0.0 \quad \text{(deterministic JSON)}
$$
$$
T_{generation} = 0.3 \quad \text{(natural language fluency)}
$$

---

## 8. Self-Reflection Loops

### 8.1 Universal Reflection Template

All JSON-producing LLM nodes implement self-reflection on parse/validation failure using `REFLECTION_TEMPLATE` (PT-05). Retries are bounded by `settings.max_reflection_attempts` (default 3).

**Nodes with self-reflection:**
- `triplet_extractor.py` — via `_reflect_on_json()` helper; truncated variant for token-cap hits
- `rag_mapper.py` — inline retry with markdown fence stripping
- `llm_judge.py` — inline retry with markdown fence stripping
- `hallucination_grader.py` — inline retry; emits only `pass | regenerate`
- `validator.py` (Actor-Critic) — explicit reflection loop
- `cypher_healer.py` — Cypher-specific reflection loop

### 8.2 Actor-Critic Best-Proposal Tracking

`BuilderState` carries a `best_proposal` field alongside `mapping_proposal`. The validation node updates `best_proposal` whenever a Pydantic-valid proposal with higher confidence is seen. On critic exhaustion (attempts >= max), the node returns `best_proposal` instead of the last rejected proposal.

### 8.3 Critic Entity Context Ordering

`critic_review()` in `validator.py` sorts entities by name length ascending before slicing to `[:20]`. Shorter names (concept-level, e.g. "Customer") appear first; longer names (attribute-level) are cut off. This prevents false rejections when the critic cannot find the concept name in its context window.

---

## 9. Evaluation Framework

### 9.1 RAGAS Metrics

| Metric | Target | Validates |
|---|---|---|
| **Faithfulness** | > 0.95 | Hallucination grader effectiveness |
| **Context Precision** | > 0.85 | Reranker quality |
| **Context Recall** | > 0.90 | Hybrid retrieval coverage |

### 9.2 Custom Metrics

| Metric | Definition |
|---|---|
| `cypher_healing_rate` | healed queries / total failed queries |
| `hitl_confidence_agreement` | correlation between auto-approved mappings and gold accuracy |

### 9.3 Ablation Studies

21 ablation experiments across 6 datasets (126 total runs). See [ABLATION.md](./ABLATION.md) for full matrix and results.

---

## 10. REST API

FastAPI application factory in `src/api/app.py` with two router groups:

### 10.1 Demo API (`/api/v1/demo/`)

| Endpoint | Method | Description |
|---|---|---|
| `/demo/build` | POST | Start Knowledge Graph build (async with polling) |
| `/demo/build/{job_id}` | GET | Poll build status |
| `/demo/query` | POST | Synchronous Q&A |
| `/demo/pipeline` | POST | Full async E2E pipeline with polling |

### 10.2 Ablation API (`/api/v1/ablation/`)

| Endpoint | Method | Description |
|---|---|---|
| `/ablation/run/preset` | POST | Run predefined AB-XX study |
| `/ablation/run/custom` | POST | Run custom configuration |
| `/ablation/matrix` | GET | Browse 21 predefined conditions |

Swagger UI at `/docs`, ReDoc at `/redoc`.

---

## 11. Known Limits & Future Work

### 11.1 Current Limitations

| Limitation | Impact |
|---|---|
| **Multi-Hop Reasoning** | Global graph reasoning over 1000+ tables exceeds output token limits |
| **Wide Tables** | Denormalized tables with >100 columns degrade mapping quality |
| **Self-Correction Ceiling** | Reflection loops may fail on semantically ambiguous errors |
| **Embedding Drift** | BGE-M3 may degrade on highly domain-specific jargon |

### 11.2 Future Research Directions

| Direction | Addresses | Approach |
|---|---|---|
| **Community Detection** | Multi-hop global reasoning | Graph algorithms (Louvain) to partition sub-graphs |
| **Hierarchical Map-Reduce** | Large schema summarisation | Recursive LLM passes over graph communities |
| **Semantic Intra-Table Chunking** | Wide tables (>100 cols) | Column clustering by semantic similarity |
| **Domain SLM Fine-Tuning** | Embedding drift on jargon | LoRA fine-tune on corporate docs |
| **Continuous Active Learning** | HITL feedback utilisation | Feed HITL corrections back to improve future mappings |
