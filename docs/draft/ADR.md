# Architecture Decision Records (ADR)

> **Project:** Multi-Agent Framework for Semantic Discovery & GraphRAG
> **Version:** 2.0 — Updated March 2026
> **Purpose:** Documents every significant architectural decision, its rationale, and the alternatives that were evaluated and rejected.

---

## Index

| ID | Title | Status | Date |
|---|---|---|---|
| [ADR-01](#adr-01--langgraph-over-crewai-or-autogen-for-orchestration) | LangGraph over CrewAI / AutoGen for orchestration | **Accepted** | 2026-01 |
| [ADR-02](#adr-02--neo4j-over-a-pure-vector-database) | Neo4j over a pure vector database | **Accepted** | 2026-01 |
| [ADR-03](#adr-03--slm-decoder-only-for-extraction-not-llm) | SLM (decoder-only) for extraction, not LLM | **Accepted** | 2026-01 |
| [ADR-04](#adr-04--bge-m3--bge-reranker-large-over-openai-embeddings) | BGE-M3 + bge-reranker-large over OpenAI embeddings | **Accepted** | 2026-01 |
| [ADR-05](#adr-05--pydantic-v2-for-all-llm-output-validation) | Pydantic v2 for all LLM output validation | **Accepted** | 2026-01 |
| [ADR-06](#adr-06--merge-upsert-strategy-never-bare-create) | MERGE upsert strategy — never bare CREATE | **Accepted** | 2026-01 |
| [ADR-07](#adr-07--actor-critic-self-reflection-over-simple-retry) | Actor-Critic self-reflection over simple retry | **Accepted** | 2026-02 |
| [ADR-08](#adr-08--hybrid-retrieval-vector--bm25--graph-traversal) | Hybrid retrieval: Vector + BM25 + Graph traversal | **Accepted** | 2026-02 |
| [ADR-09](#adr-09--self-rag-critique-generation-over-naive-hallucination-filtering) | Self-RAG critique generation over naive hallucination filtering | **Accepted** | 2026-02 |
| [ADR-10](#adr-10--temperature-00-for-all-structuredcode-nodes) | Temperature 0.0 for all structured/code nodes | **Accepted** | 2026-02 |
| [ADR-11](#adr-11--two-stage-entity-resolution-blocking--llm-judge) | Two-stage Entity Resolution: blocking + LLM judge | **Accepted** | 2026-02 |
| [ADR-12](#adr-12--openrouter-free-tier-as-the-unified-llm-provider) | OpenRouter Free Tier as the unified LLM provider | **Accepted** | 2026-02 |
| [ADR-13](#adr-13--sqlglot-for-ddl-parsing-no-llm-on-deterministic-tasks) | sqlglot for DDL parsing — no LLM on deterministic tasks | **Accepted** | 2026-02 |
| [ADR-14](#adr-14--ragas-as-the-evaluation-framework) | RAGAS as the evaluation framework | **Accepted** | 2026-03 |
| [ADR-15](#adr-15--llm-zero-shot-schema-enrichment-for-lexical-gap-mitigation) | LLM Zero-Shot Schema Enrichment for Lexical Gap Mitigation | **Accepted** | 2026-03 |

---

## ADR-01 — LangGraph over CrewAI or AutoGen for Orchestration

**Status:** Accepted
**Date:** January 2026
**Deciders:** Marc'Antonio Lopez

### Context

The system requires a multi-agent orchestration framework capable of:
- Expressing a **Directed Acyclic Graph (DAG)** of cognitive nodes
- Supporting **conditional branching** (confidence threshold routing, error routing)
- Implementing **self-reflection loops** (finite retry with state tracking)
- Supporting **Human-in-the-Loop (HITL) interrupts** with state persistence across process restarts
- **State checkpointing** for fault recovery

### Decision

Use **LangGraph** as the sole orchestration framework.

### Alternatives Evaluated

| Framework | Why Rejected |
|---|---|
| **CrewAI** | Role-based agent abstraction too high-level; no native support for conditional graph edges or HITL interrupt/resume. Loops require workarounds not suited for production self-reflection patterns. |
| **AutoGen** | Conversation-based (agent ↔ agent chat). Difficult to express a strict DAG topology. State management is implicit in conversation history, not an explicit typed state object. HITL requires custom middleware. |
| **Raw LangChain LCEL** | No native graph topology, no state checkpointing, no conditional routing without custom code. Sufficient for linear chains, not for this architecture. |
| **LlamaIndex Workflows** | Viable but ecosystem less mature than LangGraph for graph-based agentic patterns as of 2026. Fewer examples of HITL + self-reflection patterns. |

### Consequences

- **Positive:** Explicit `StateGraph` definition makes the entire cognitive flow auditable, testable per node, and reproducible. HITL via `interrupt()` + `MemorySaver`/`SqliteSaver` is natively supported.
- **Negative:** LangGraph's API surface is larger; requires understanding of `StateGraph`, `CompiledGraph`, checkpointers, and stream modes.
- **Constraint for agent:** Always use `langgraph.graph.StateGraph`. Never introduce a second orchestration framework. Routing logic lives exclusively in conditional edge functions, not inside node functions.

---

## ADR-02 — Neo4j over a Pure Vector Database

**Status:** Accepted
**Date:** January 2026

### Context

The system must store both the **ontological structure** (business concepts, physical tables, and their semantic relationships) and support **vector similarity search** for retrieval. Two classes of storage were evaluated: graph databases and pure vector stores.

### Decision

Use **Neo4j** as the single storage backend, leveraging its native **vector index** (for dense retrieval) and **BM25 full-text index** alongside the graph topology.

### Alternatives Evaluated

| Store | Why Rejected |
|---|---|
| **Pinecone** | Pure vector store; no graph topology. Cannot express `:MAPPED_TO`, `:RELATED_TO`, `:JOINS_WITH` relationships or perform graph traversal for context expansion. Requires a separate graph DB anyway. |
| **Chroma** | Lightweight, but lacks BM25, graph traversal, and production-grade persistence. Not suitable for storing the ontology structure. |
| **Weaviate** | Has both vector and graph-lite features, but the graph model is weaker than Neo4j's property graph; Cypher is far more expressive than Weaviate's GraphQL for ontology queries. |
| **Neo4j + Pinecone (dual store)** | Double infrastructure cost and synchronisation complexity. Neo4j's native vector index (available since Neo4j 5.11, GA 2024) eliminates the need for a separate vector store. |
| **PostgreSQL + pgvector** | No graph traversal; JOIN-based relationship queries are far less expressive than Cypher for multi-hop reasoning. |

### Consequences

- **Positive:** Single storage layer for topology, vectors, and BM25 — simplifies ops, no sync issues. Cypher enables multi-hop graph traversal for context expansion in the Query Graph.
- **Negative:** Requires a running Neo4j instance (local Docker or AuraDB). Vector index dimension must match embedding model (BGE-M3 = 1024 dims).
- **Constraint for agent:** All queries must use the official `neo4j` Python driver. Do not introduce additional database clients. Vector index name: `businessconcept_embedding`. All write operations use `MERGE` (see ADR-06).

---

## ADR-03 — SLM (Decoder-Only) for Extraction, Not LLM

**Status:** Accepted
**Date:** January 2026

### Context

Triplet extraction from text chunks is a structured, constrained task (output = fixed JSON schema). Two approaches were evaluated: using the large frontier LLM for all tasks, or introducing a smaller, cheaper model for extraction.

### Decision

Use a **Small Language Model (SLM)** — specifically `qwen/qwen3-next-80b-a3b-instruct:free` via **OpenRouter Free Tier** — exclusively for the extraction node, called in **JSON Mode** with a mandatory Pydantic output schema.

### Rationale

| Factor | SLM (chosen) | LLM Frontier |
|---|---|---|
| **Cost** | ~10–50× cheaper per token | Expensive for bulk extraction |
| **Speed** | Faster inference, parallelisable | Slower |
| **Task fit** | Constrained JSON output = decoder-only strength | LLM reasoning capacity wasted on schema-constrained tasks |
| **NER lock-in** | Bypassed entirely via JSON schema enforcement | Would require NER taxonomy fine-tuning |
| **Hallucination risk** | Lower — output is schema-constrained | Higher — unconstrained generation |

### Alternatives Evaluated

| Approach | Why Rejected |
|---|---|
| **gpt-4o for extraction** | Unnecessary cost; extraction is a pattern-matching task, not a reasoning task. |
| **Traditional NER (spaCy, BERT-NER)** | Taxonomy lock-in: only extracts pre-defined entity types. Cannot generalise to arbitrary business domains without fine-tuning. |
| **Rule-based extraction** | Brittle, domain-specific, not scalable to heterogeneous PDF formats. |

### Consequences

- **Positive:** Significant cost reduction on bulk extraction over large document corpora.
- **Negative:** SLM may miss complex, multi-sentence relations that require cross-sentence reasoning. Mitigation: provenance chunking overlap (64 tokens) ensures context spans sentence boundaries.
- **Constraint for agent:** The `Extract_Triplets_SLM` node MUST call `settings.llm_model_extraction` (not `settings.llm_model_reasoning`). JSON Mode must be enforced; never call the extraction SLM without a Pydantic output schema.

---

## ADR-04 — BGE-M3 + bge-reranker-large over OpenAI Embeddings

**Status:** Accepted
**Date:** January 2026

### Context

The system needs dense embeddings for vector retrieval and a reranking model for precision filtering. Two options were evaluated: OpenAI's managed embedding service vs. open-weight models run locally.

### Decision

Use **BAAI/BGE-M3** for embeddings and **BAAI/bge-reranker-large** (Cross-Encoder) for reranking, both run locally via `sentence-transformers` / `FlagEmbedding`.

### Alternatives Evaluated

| Model | Why Rejected |
|---|---|
| **OpenAI `text-embedding-3-large`** | API cost per embedding, external dependency, no reranker equivalent, 3072-dim vs BGE-M3's 1024-dim (better Neo4j vector index performance), data privacy concerns for enterprise DB schemas. |
| **OpenAI `text-embedding-ada-002`** | Older model, lower recall on multilingual content, 1536-dim, still has all the cost/privacy issues. |
| **Cohere Embed + Rerank** | External API dependency, higher latency, cost at scale. |
| **`all-MiniLM-L6-v2`** | 384-dim, poor multilingual support, lower recall on domain-specific text. |

### BGE-M3 Advantages

- **Multilingual** (100+ languages) — critical for Italian business documentation
- **Multi-granularity retrieval** — supports dense, sparse, and colBERT-style retrieval in one model
- **1024-dim** — good balance between expressiveness and Neo4j vector index performance
- **State-of-the-art BEIR benchmarks** (2024–2025)

### Consequences

- **Positive:** No external API calls for embeddings; all inference local. Privacy-preserving. One-time model download (~570MB + ~1.1GB for reranker).
- **Negative:** Requires sufficient RAM/VRAM. BGE-M3 runs on CPU if no GPU; reranker uses `use_fp16=True` fallback.
- **Constraint for agent:** Embedding dimension is **1024**. The Neo4j vector index MUST be created with `vector.dimensions: 1024`. Never change the embedding model without updating the index. Use `FlagEmbedding` library for BGE-M3, not raw `sentence-transformers`, to access multi-vector retrieval features.

---

## ADR-05 — Pydantic v2 for All LLM Output Validation

**Status:** Accepted
**Date:** January 2026

### Context

LLMs do not reliably produce valid JSON or respect schema constraints. Every node that calls an LLM must validate the output before passing it downstream.

### Decision

Use **Pydantic v2** (`pydantic>=2.7`) as the exclusive validation layer for all LLM outputs. Every LLM call returns a Pydantic model instance, never a raw dict or string.

### Pattern

```python
# Every LLM node follows this pattern:
response = llm.invoke(prompt)
try:
    validated = OutputModel.model_validate_json(response.content)
except ValidationError as e:
    # Inject error string into Reflection Prompt
    return reflect(error=str(e), original_input=input_data)
```

### Alternatives Evaluated

| Approach | Why Rejected |
|---|---|
| **Manual dict validation** | Error-prone, non-reusable, no type inference. |
| **Marshmallow** | Pydantic v2 is faster (Rust core), more ergonomic, and natively integrated with LangChain's structured output. |
| **Instructor library** | Built on Pydantic anyway; adds an extra dependency. LangChain's `.with_structured_output(Model)` achieves the same result natively. |
| **No validation** | Unacceptable — downstream nodes would receive malformed data and fail silently. |

### Consequences

- **Constraint for agent:** Every model class lives in `src/models/schemas.py`. Never define Pydantic models inline in node functions. Use `model_validate_json()` not `model_validate()` on LLM string outputs. On `ValidationError`, always invoke the Reflection Prompt loop (never crash or silently discard).

---

## ADR-06 — MERGE Upsert Strategy — Never Bare CREATE

**Status:** Accepted
**Date:** January 2026

### Context

The system is designed for **incremental, continuous ingestion** — new documents and DDL files are added over time. Write operations must be idempotent: running the Builder twice on the same input must produce identical graph state.

### Decision

All Cypher write operations use **`MERGE`** exclusively. `CREATE` is forbidden for nodes and relationships. This applies to both LLM-generated Cypher and any hand-written queries.

### Rationale

| Operation | Effect on re-run |
|---|---|
| `CREATE (n:BusinessConcept {name: "X"})` | Creates a **duplicate** node — graph becomes inconsistent |
| `MERGE (n:BusinessConcept {name: "X"})` | Finds existing node or creates it — **idempotent** |

`MERGE` + `ON CREATE SET` + `ON MATCH SET` allows:
- First run: creates node with all properties
- Subsequent runs: updates only changed properties (e.g., updated confidence score)

### Consequences

- **Positive:** The entire pipeline is re-runnable without cleanup. Delta ingestion works naturally.
- **Negative:** `MERGE` is slightly slower than `CREATE` on first write. Negligible at this scale.
- **Constraint for agent:** The `Generate_Cypher` system prompt MUST include `"Never use bare CREATE. Use MERGE for all node and relationship writes."` The `Fix_Cypher_LLM` node must also enforce this. Any Cypher containing `CREATE` without `MERGE` must be rejected at the `Test_Cypher_Execution` node before commit.

---

## ADR-07 — Actor-Critic Self-Reflection over Simple Retry

**Status:** Accepted
**Date:** February 2026

### Context

When a node fails (Pydantic validation error, semantic mapping error, Cypher syntax error), the system must attempt correction. Two approaches were evaluated: blind retry vs. informed self-reflection.

### Decision

Use **Actor-Critic self-reflection**: the exact error or critique is injected into the LLM prompt as a **Reflection Prompt**, giving the model precise, actionable information for correction.

### Comparison

| Approach | Mechanism | Success Rate |
|---|---|---|
| **Simple retry** | Re-invoke the same prompt unchanged | Low — LLM will likely repeat the same error |
| **Random temperature increase** | Increase `T` to 0.5 on retry | Unpredictable — increases noise, not correctness |
| **Actor-Critic (chosen)** | Inject exact error/critique into prompt | High — model has deterministic signal for correction |

### Reflection Prompt Design Principles

1. **Include the exact error message** (not a paraphrase)
2. **Include the original input** so the model has full context
3. **Strict persona** — "Return only corrected JSON. No explanation."
4. **Attempt counter** — state tracks `reflection_attempts`; hard cap at `settings.max_reflection_attempts`

### Consequences

- **Constraint for agent:** Never implement a retry loop that re-sends the same prompt. Every retry MUST use the `REFLECTION_TEMPLATE` from `src/prompts/templates.py`. The loop counter in `BuilderState` (`reflection_attempts`, `healing_attempts`) must be incremented before each retry call and checked before routing.

---

## ADR-08 — Hybrid Retrieval: Vector + BM25 + Graph Traversal

**Status:** Accepted
**Date:** February 2026

### Context

No single retrieval method is sufficient for this domain:
- Dense vector search struggles with exact keyword matches (table names, column IDs)
- BM25 keyword search misses paraphrases and semantic similarity
- Neither captures relational context (which tables JOIN together)

### Decision

Use **three retrieval methods in parallel**, merge results, deduplicate, then pass to the Cross-Encoder reranker.

### Method Roles

| Method | Problem Solved | Failure Mode |
|---|---|---|
| **Dense vector (BGE-M3)** | Semantic paraphrases, synonyms | Rare exact tokens (IDs, codes) |
| **BM25 keyword** | Exact table/column names, codes | Misses paraphrases entirely |
| **Graph traversal** | Relational topology (JOINs, related concepts) | Only works if seed nodes already found by vector/BM25 |

### Alternatives Evaluated

| Approach | Why Rejected |
|---|---|
| **Vector only (Naive RAG)** | Lexical gap — misses exact identifiers; no relational context |
| **BM25 only** | No semantic understanding |
| **ColBERT late interaction** | High compute cost; BGE-M3 already supports multi-vector retrieval; overkill given Neo4j setup |

### Consequences

- **Constraint for agent:** All three retrieval methods run in parallel (use `asyncio.gather` or sequential calls). Results merged in `merge_results()` — deduplication by `node_id`. Graph traversal depth capped at `settings.retrieval_graph_depth` (default: 2) to prevent explosive result sets.

---

## ADR-09 — Self-RAG Critique Generation over Naive Hallucination Filtering

**Status:** Accepted
**Date:** February 2026

### Context

The Query Graph must prevent factually unsupported answers. Two approaches were evaluated: filtering (block bad outputs) vs. critique-driven regeneration.

### Decision

Use **Self-RAG critique generation**: the Hallucination Grader produces a **natural-language critique** that names specific unsupported entities, which is then injected into the next generation prompt.

### Comparison

| Approach | Mechanism | Problem |
|---|---|---|
| **Binary filter** | Block answer if hallucination score > threshold | No signal for the generator — blind retry |
| **Naive retry** | Re-ask the same question | LLM produces same hallucination |
| **Self-RAG critique (chosen)** | Generate specific critique → inject into next prompt | Generator receives exact actionable correction |

### Critique Design

A good critique must:
- Name the **specific entity/table/concept** that is unsupported
- State **why** it is unsupported ("not present in retrieved context")
- Give a **concrete correction instruction** ("Reformulate omitting TB_X")

### Consequences

- **Constraint for agent:** The `Hallucination_Grader` node must **never** produce a binary `true/false` output alone. It must always populate `GraderDecision.critique` with specific entity names when `grounded=False`. The critique is injected into `QueryState.hallucination_critique` and passed to `Answer_Generation_LLM` on the next iteration.

---

## ADR-10 — Temperature 0.0 for All Structured/Code Nodes

**Status:** Accepted
**Date:** February 2026

### Context

Different nodes have different output requirements. Extraction, mapping, and Cypher generation require **deterministic, reproducible** outputs. User-facing answer generation benefits from slightly more natural language variation.

### Decision

| Node Category | Temperature | Rationale |
|---|---|---|
| Extraction, ER, Mapping, Validation, Cypher Gen/Fix | **0.0** | Deterministic logic; any randomness increases error rate |
| Hallucination Grader | **0.0** | Binary grounding assessment must be reproducible |
| Answer Generation (user-facing) | **0.3** | Slight variation acceptable for natural language fluency |

### Consequences

- **Constraint for agent:** Temperature values come from `settings` (`llm_temperature_extraction=0.0`, `llm_temperature_generation=0.3`). Never hardcode temperature values in node functions. Never use `temperature > 0` as a "retry strategy" (see ADR-07).

---

## ADR-11 — Two-Stage Entity Resolution: Blocking + LLM Judge

**Status:** Accepted
**Date:** February 2026

### Context

Raw triplet extraction produces many near-duplicate entity strings ("Customer", "Customers", "customer entity", "CUST"). Entity Resolution must collapse these without making an LLM call for every pair (O(n²) cost).

### Decision

Two-stage pipeline:
1. **Blocking** (cheap): K-NN vector search groups semantically similar strings into candidate clusters — no LLM
2. **Matching** (expensive): LLM judge decides, per cluster, whether variants refer to the same concept, using their original provenance text for disambiguation

### Rationale

| Stage | Method | Cost | Correctness |
|---|---|---|---|
| Full pairwise LLM | LLM for every pair | O(n²) LLM calls | High |
| Vector-only | Cosine threshold only | O(n log n) | Medium (misses semantic edge cases) |
| **Blocking + LLM judge (chosen)** | K-NN then LLM | O(n log n) + O(clusters) LLM calls | High |

### Provenance Injection Principle

The LLM judge **must receive** the original `provenance_text` for each variant — this is what allows disambiguation of genuinely ambiguous terms (e.g., "Apple" company vs. "Apple" fruit) that cannot be resolved by name alone.

### Consequences

- **Constraint for agent:** Stage 1 uses `BGE-M3` + `faiss`/`sklearn`. The `er_similarity_threshold` (default 0.85) is configurable. Stage 2 LLM calls are made **only for clusters with ≥2 variants**. The `CanonicalEntityDecision.reasoning` field is logged but never shown to the user.

---

## ADR-12 — OpenRouter Free Tier as the Unified LLM Provider

**Status:** Accepted
**Date:** February 2026

### Context

The system requires access to both a **reasoning-capable LLM** (for mapping, Cypher generation, grading) and an **SLM** (for structured extraction) without incurring the hardware cost of local inference or the per-token cost of commercial APIs at scale during thesis development.

### Decision

Use **OpenRouter Free Tier** as the single LLM provider, accessed via `langchain-openrouter`'s `ChatOpenRouter` class. A single `OPENROUTER_API_KEY` authenticates both the reasoning LLM and the extraction SLM. The underlying model is selected per-call via model slug in `settings`.

### Configuration

```bash
# OpenRouter Free Tier
OPENROUTER_API_KEY=sk-or-v1-...
LLM_MODEL_REASONING=qwen/qwen3-coder:free
LLM_MODEL_EXTRACTION=qwen/qwen3-next-80b-a3b-instruct:free
```

### Alternatives Evaluated

| Option | Why Rejected |
|---|---|
| **Local Ollama (Qwen2.5-Coder-32B + NuExtract)** | Requires local GPU/sufficient VRAM not available in the thesis environment. Cannot run a 32B-parameter model on CPU at usable speed. |
| **OpenAI API (gpt-4o)** | Per-token cost unsustainable for bulk extraction + evaluation runs across 50+ gold-standard samples. No free tier for reasoning-grade models. |
| **Azure OpenAI** | Requires enterprise account setup; overkill for a thesis project. Same cost concerns as OpenAI API. |
| **Direct Anthropic/Google APIs** | Separate SDK per provider; breaks the single-provider abstraction. Higher integration complexity with LangChain. |
| **OpenRouter (chosen)** | Unified API for multiple model families; Free Tier covers both reasoning and extraction model needs; single auth key; full LangChain integration via `langchain-openrouter`. |

### Consequences

- **Positive:** Zero local compute cost. Both model roles (reasoning + extraction) served from a single API endpoint under one key. `ChatOpenRouter` integrates natively with LangChain LCEL and `with_structured_output()`.
- **Negative:** Depends on external service availability. Free Tier has rate limits — evaluation runs should be scheduled with retry logic (`max_llm_retries`).
- **Constraint for agent:** Never use `openai` SDK directly. Always use `langchain_openrouter.ChatOpenRouter` with `openrouter_api_key=settings.openrouter_api_key`. Model names are always read from `settings` (`llm_model_reasoning` / `llm_model_extraction`), never hardcoded.

---

## ADR-13 — sqlglot for DDL Parsing — No LLM on Deterministic Tasks

**Status:** Accepted
**Date:** February 2026

### Context

SQL DDL parsing (extracting table names, columns, types, constraints from `CREATE TABLE` statements) is a **deterministic, grammar-based** task. Two approaches: use an LLM or use a dedicated SQL parser library.

### Decision

Use **`sqlglot`** for DDL parsing. No LLM is involved in this node.

### Rationale

| Factor | sqlglot | LLM for DDL |
|---|---|---|
| **Determinism** | 100% deterministic | Non-deterministic |
| **Cost** | Zero inference cost | Significant for large schemas |
| **Speed** | Milliseconds | Seconds |
| **Accuracy** | Perfect for valid SQL | Prone to hallucination on complex DDL |
| **Dialect support** | MySQL, PostgreSQL, T-SQL, Oracle, etc. | Requires dialect-specific prompting |

**Principle: Never use an LLM where a deterministic algorithm exists.**

### Consequences

- **Constraint for agent:** `src/ingestion/ddl_parser.py` must be LLM-free. `sqlglot.parse_one(ddl, read="auto")` handles dialect detection automatically. If `sqlglot` fails to parse a DDL statement, raise `DDLParseError` with the raw statement included — do not fall back to an LLM call.

---

## ADR-14 — RAGAS as the Evaluation Framework

**Status:** Accepted
**Date:** March 2026

### Context

Measuring the quality of a RAG system requires specialised metrics that traditional software testing metrics (accuracy, F1) do not capture. The need is for metrics that assess: retrieval quality, generation faithfulness, and absence of hallucinations.

### Decision

Use **RAGAS** (`ragas>=0.2`) as the primary evaluation framework, supplemented by two custom system-specific metrics (`cypher_healing_rate`, `hitl_confidence_agreement`).

### RAGAS Metric Selection

| Metric | What It Measures | Why Included |
|---|---|---|
| `faithfulness` | Claims in answer supported by context | Core hallucination measure |
| `context_precision` | Relevant chunks / total retrieved chunks | Reranker quality |
| `context_recall` | Gold entities retrieved / all gold entities | Hybrid retrieval coverage |
| `answer_relevancy` | Answer addresses the question | User-facing quality |

### Alternatives Evaluated

| Framework | Why Not Chosen |
|---|---|
| **TruLens** | Good, but RAGAS has more established academic citation track record for thesis context |
| **DeepEval** | Overlapping metrics; RAGAS more integrated with LangChain ecosystem |
| **Manual human evaluation only** | Not scalable to 50+ samples; lacks quantitative reproducibility |

### Consequences

- **Constraint for agent:** The evaluation pipeline in `src/evaluation/ragas_runner.py` uses `ragas.evaluate()` with an `EvaluationDataset`. Custom metrics (`cypher_healing_rate`, `hitl_confidence_agreement`) are computed separately from Builder Graph execution logs and combined into the final `EvaluationReport`.

---

## ADR-15 — LLM Zero-Shot Schema Enrichment for Lexical Gap Mitigation

**Status:** Accepted
**Date:** March 2026
**Deciders:** Marc'Antonio Lopez

### Context

Database schemas overwhelmingly use abbreviated, cryptic identifiers (e.g., `TB_CST`, `ORD_DT`, `CUST_ADDR`) that have no semantic overlap with natural-language business glossary terms (e.g., "Customer", "Order Date", "Customer Address"). This creates a **Lexical Gap**: when the mapping node embeds a raw table name alongside a business concept definition, cosine similarity is low purely due to surface-form mismatch — not because the concepts are unrelated.

This gap degrades both the RAG retrieval step (BGE-M3 embeddings of `TB_CST` and "Customer" are distant) and the downstream LLM mapping quality.

### Decision

Insert an **LLM Schema Enrichment** node (`LLM_Schema_Enrichment`) between `Parse_Technical_Schema` and `Retrieval_Augmented_Mapping_LLM` in the Builder Graph. This node uses a **Zero-Shot LLM call** (T=0.0) to expand abbreviated table and column names into precise, human-readable English names and generate a brief natural-language description for each table.

The enriched metadata (not the original identifiers, which are preserved) is used for embedding and semantic retrieval, while the original identifiers remain authoritative for Cypher generation.

### Alternatives Evaluated

| Approach | Why Rejected |
|---|---|
| **Static synonym dictionary** | Requires manual curation per schema; cannot generalise to unseen abbreviations. Maintenance cost dominates over time. |
| **Fine-tuned abbreviation expansion model** | Requires training data of `(abbreviation → expansion)` pairs per domain. Not scalable across heterogeneous enterprise schemas. |
| **Regex heuristics** (split on `_`, expand common prefixes) | Covers trivial cases (`CUST` → "Customer") but fails on domain-specific abbreviations (`TB_CST`, `SLS_ORD_HDR`). Cannot generate table descriptions. |
| **No enrichment (embed raw names)** | Baseline approach. Measured: cosine similarity between raw DDL identifier embeddings and business glossary embeddings is significantly lower, degrading mapping precision. |
| **Enrichment at embedding time only** | Would require a custom embedding wrapper; enrichment result not reusable by the LLM mapping prompt. Separate enrichment node is cleaner. |

### Rationale

| Factor | Zero-Shot LLM Enrichment (chosen) | Static Dictionary |
|---|---|---|
| **Generalisation** | Handles any schema without prior setup | Only covers pre-defined abbreviations |
| **Quality** | Strong — LLMs excel at abbreviation expansion | Exact match only; misses novel abbreviations |
| **Cost** | One LLM call per table (not per column); cheap at T=0.0 | Zero inference cost |
| **Maintenance** | Zero — no dictionary to curate | High — dictionary grows with each new schema |
| **Description generation** | Produces natural-language table descriptions for embedding | Cannot |

### Enrichment Output Schema

```python
class EnrichedColumn(BaseModel):
    original_name: str       # "CUST_ID" — unchanged
    enriched_name: str       # "Customer ID" — human-readable

class EnrichedTableSchema(BaseModel):
    table_name: str          # original identifier preserved
    enriched_table_name: str # "Customer Table"
    enriched_columns: list[EnrichedColumn]
    table_description: str   # "Master record for all registered platform customers."
```

### Consequences

- **Positive:** Embedding similarity between enriched table metadata and business glossary terms increases substantially, improving mapping precision. The enriched description provides the LLM mapper with semantic context that raw DDL identifiers lack.
- **Negative:** Adds one LLM call per table to the Builder pipeline. At T=0.0, results are deterministic and cacheable.
- **Constraint for agent:** The enrichment node MUST be placed after `parse_ddl` and before `rag_mapping`. The original `table_name` and `column.name` values must NEVER be overwritten — enriched names are stored in separate fields. The enriched metadata is used for embedding + retrieval queries; the original identifiers are used in Cypher generation. Use `settings.llm_model_reasoning` with `temperature=0.0`.
