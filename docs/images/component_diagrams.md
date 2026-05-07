# Component Architecture Diagrams

All Mermaid diagrams for internal component architectures.

---

## 02 - Configuration System

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#FAFAFA', 'primaryTextColor': '#212121', 'primaryBorderColor': '#9E9E9E', 'lineColor': '#616161', 'fontSize': '13px', 'fontFamily': 'Inter, Helvetica, Arial, sans-serif'}}}%%
flowchart TD
    ENV[".env / Environment Variables"]:::input
    CFG("AppConfig<br/>Frozen dataclass defaults"):::process
    SET("Settings<br/>Pydantic BaseSettings + SecretStr"):::key
    FAC("LLM Factory<br/>make_llm + tier caches"):::key
    DET("Provider Detection<br/>6-rule chain"):::process
    BLD("Model Builders<br/>ChatOpenAI / ChatAnthropic / ..."):::process
    CLI("InstrumentedLLM<br/>Proxy: retry + logging + tokens"):::key
    FBK("FallbackLLM<br/>Free-to-paid circuit breaker"):::process
    LOG("Structured Logging<br/>JSON formatter + node events"):::process
    TRC("Pipeline Tracing<br/>BuilderTrace / QueryTrace"):::process
    OBS("Observability<br/>LangSmith + Langfuse callbacks"):::process
    PIPE["Pipeline Modules"]:::output

    ENV --> SET
    CFG --> SET
    SET --> FAC
    DET --> FAC
    BLD --> FAC
    FAC --> CLI
    CLI --> FBK
    FBK --> PIPE
    SET --> LOG
    SET --> TRC
    SET --> OBS
    OBS --> CLI

    classDef input fill:#FAFAFA,stroke:#424242,stroke-width:2px
    classDef process fill:#F5F5F5,stroke:#9E9E9E,stroke-width:1.5px
    classDef key fill:#E3F2FD,stroke:#1565C0,stroke-width:2px,color:#0D47A1
    classDef output fill:#37474F,stroke:#263238,stroke-width:2px,color:#ECEFF1
```

---

## 03 - Data Models

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#FAFAFA', 'primaryTextColor': '#212121', 'primaryBorderColor': '#9E9E9E', 'lineColor': '#616161', 'fontSize': '13px', 'fontFamily': 'Inter, Helvetica, Arial, sans-serif'}}}%%
flowchart LR
    subgraph schemas["schemas.py — Pydantic Models"]
        DOC("Document"):::process
        CHK("Chunk"):::process
        TRP("Triplet"):::process
        ENT("Entity"):::process
        TBL("TableSchema"):::process
        ETBL("EnrichedTableSchema"):::process
        MAP("MappingProposal"):::process
        CYP("CypherStatement"):::process
        RET("RetrievedChunk"):::process
        GRD("GraderDecision"):::process
    end

    subgraph state["state.py — LangGraph TypedDict"]
        BS("BuilderState"):::key
        QS("QueryState"):::key
    end

    DOC --> CHK
    CHK --> TRP
    TRP --> ENT
    TBL --> ETBL
    ETBL --> MAP
    MAP --> CYP
    RET --> GRD

    TRP --> BS
    ENT --> BS
    MAP --> BS
    CYP --> BS
    RET --> QS
    GRD --> QS

    classDef process fill:#F5F5F5,stroke:#9E9E9E,stroke-width:1.5px
    classDef key fill:#E3F2FD,stroke:#1565C0,stroke-width:2px,color:#0D47A1
```

---

## 04 - Prompt Engineering

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#FAFAFA', 'primaryTextColor': '#212121', 'primaryBorderColor': '#9E9E9E', 'lineColor': '#616161', 'fontSize': '13px', 'fontFamily': 'Inter, Helvetica, Arial, sans-serif'}}}%%
flowchart TD
    TPL["templates.py<br/>Prompt Catalogue"]:::input

    subgraph templates["Template Identifiers"]
        PT01("PT-01 Extraction"):::process
        PT02("PT-02 ER Judge"):::process
        PT03("PT-03 Mapping"):::process
        PT04("PT-04 Critic"):::process
        PT05("PT-05 Reflection"):::key
        PT06("PT-06 Enrichment"):::process
        PT07("PT-07 Cypher Gen"):::process
        PT08("PT-08 Cypher Fix"):::process
        PT09("PT-09 Answer Gen"):::process
        PT10("PT-10 Grader"):::process
    end

    FS["few_shot.py<br/>JSON example loader"]:::input
    DATA[("src/data/<br/>few_shot_*.json")]:::database

    DATA --> FS
    FS --> PT03
    FS --> PT07
    TPL --> templates

    PT05 -. "injected on error" .-> PT01
    PT05 -. "injected on error" .-> PT02
    PT05 -. "injected on error" .-> PT03
    PT05 -. "injected on error" .-> PT07

    classDef input fill:#FAFAFA,stroke:#424242,stroke-width:2px
    classDef process fill:#F5F5F5,stroke:#9E9E9E,stroke-width:1.5px
    classDef key fill:#E3F2FD,stroke:#1565C0,stroke-width:2px,color:#0D47A1
    classDef database fill:#37474F,stroke:#263238,stroke-width:2px,color:#ECEFF1
```

---

## 05 - Utilities

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#FAFAFA', 'primaryTextColor': '#212121', 'primaryBorderColor': '#9E9E9E', 'lineColor': '#616161', 'fontSize': '13px', 'fontFamily': 'Inter, Helvetica, Arial, sans-serif'}}}%%
flowchart TD
    RAW["Raw LLM Output"]:::input

    subgraph json_utils["json_utils.py"]
        EXT("extract_text_content<br/>Normalize content field"):::process
        CLN("clean_json<br/>Strip fences + extract object"):::key
        REF("reflect_on_json<br/>LLM self-correction loop"):::key
    end

    subgraph text_utils["text_utils.py"]
        NRM("normalize_concept_name<br/>CamelCase / underscore"):::process
        TOK("tokenize + stop-word removal"):::process
        SPL("split_sentences<br/>Regex-based"):::process
        DST("distill_text<br/>FK format / noise removal"):::process
    end

    VALID["Validated JSON object"]:::output

    RAW --> EXT --> CLN
    CLN -- "parse error" --> REF
    REF --> CLN
    CLN -- "success" --> VALID

    classDef input fill:#FAFAFA,stroke:#424242,stroke-width:2px
    classDef process fill:#F5F5F5,stroke:#9E9E9E,stroke-width:1.5px
    classDef key fill:#E3F2FD,stroke:#1565C0,stroke-width:2px,color:#0D47A1
    classDef output fill:#37474F,stroke:#263238,stroke-width:2px,color:#ECEFF1
```

---

## 06 - Ingestion

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#FAFAFA', 'primaryTextColor': '#212121', 'primaryBorderColor': '#9E9E9E', 'lineColor': '#616161', 'fontSize': '13px', 'fontFamily': 'Inter, Helvetica, Arial, sans-serif'}}}%%
flowchart TD
    PDF["PDF / TXT files"]:::input
    DDL["DDL / SQL files"]:::input

    REG("File Registry<br/>SHA-256 change detection"):::key

    subgraph pdf_path["pdf_loader.py"]
        LOAD("load_pdf<br/>PyMuPDF extraction"):::process
        CHKH("chunk_documents_hierarchical<br/>Parent + Child chunks"):::process
    end

    subgraph ddl_path["ddl_parser.py"]
        STRIP("Pre-clean<br/>Remove non-CREATE stmts"):::process
        PARSE("sqlglot AST parse<br/>Multi-dialect"):::key
        EXTRACT("Extract TableSchema<br/>Columns, PK, FK"):::process
    end

    ENRICH("Schema Enrichment<br/>LLM acronym expansion"):::key
    ETBL["EnrichedTableSchema[]"]:::output
    CHUNKS["Parent + Child Chunks"]:::output

    PDF --> REG
    DDL --> REG
    REG -- "new / modified" --> LOAD
    REG -- "new / modified" --> STRIP
    REG -. "unchanged: skip" .-> SKIP((" ")):::hidden
    LOAD --> CHKH --> CHUNKS
    STRIP --> PARSE --> EXTRACT
    EXTRACT --> ENRICH --> ETBL

    classDef input fill:#FAFAFA,stroke:#424242,stroke-width:2px
    classDef process fill:#F5F5F5,stroke:#9E9E9E,stroke-width:1.5px
    classDef key fill:#E3F2FD,stroke:#1565C0,stroke-width:2px,color:#0D47A1
    classDef output fill:#37474F,stroke:#263238,stroke-width:2px,color:#ECEFF1
    classDef hidden fill:none,stroke:none
```

---

## 07 - Triplet Extraction

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#FAFAFA', 'primaryTextColor': '#212121', 'primaryBorderColor': '#9E9E9E', 'lineColor': '#616161', 'fontSize': '13px', 'fontFamily': 'Inter, Helvetica, Arial, sans-serif'}}}%%
flowchart TD
    CHUNKS["Chunk[]"]:::input

    PAR("ThreadPoolExecutor<br/>Parallel extraction"):::process

    subgraph llm_path["LLM Path (default)"]
        INV("SLM invoke<br/>JSON mode"):::process
        PARS("JSON parse<br/>+ Pydantic validation"):::key
        REFL("Self-Reflection<br/>Up to 3 attempts"):::key
    end

    subgraph heuristic_path["Heuristic Path (lazy)"]
        SPA("spaCy dep-parse<br/>nsubj / ROOT / dobj"):::process
        REX("Regex fallback<br/>maps_to / is / stores / contains"):::process
    end

    DEDUP("Deduplication<br/>by (S, P, O, chunk_idx)"):::process
    TRIPS["Triplet[]"]:::output

    CHUNKS --> PAR
    PAR --> INV
    INV --> PARS
    PARS -- "error" --> REFL --> PARS
    PARS -- "success" --> DEDUP
    PAR -. "use_lazy_extraction" .-> SPA
    SPA -. "spaCy unavailable" .-> REX
    SPA --> DEDUP
    REX --> DEDUP
    DEDUP --> TRIPS

    classDef input fill:#FAFAFA,stroke:#424242,stroke-width:2px
    classDef process fill:#F5F5F5,stroke:#9E9E9E,stroke-width:1.5px
    classDef key fill:#E3F2FD,stroke:#1565C0,stroke-width:2px,color:#0D47A1
    classDef output fill:#37474F,stroke:#263238,stroke-width:2px,color:#ECEFF1
```

---

## 08 - Entity Resolution

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#FAFAFA', 'primaryTextColor': '#212121', 'primaryBorderColor': '#9E9E9E', 'lineColor': '#616161', 'fontSize': '13px', 'fontFamily': 'Inter, Helvetica, Arial, sans-serif'}}}%%
flowchart TD
    TRIPS["Triplet[]"]:::input

    subgraph stage1["Stage 1 — Vector Blocking"]
        UNQ("Extract unique entities<br/>+ quality filter"):::process
        EMB("BGE-M3 Embedding<br/>1024-dim vectors"):::process
        SIM("Cosine similarity matrix<br/>+ Top-K pruning"):::key
        UF("Union-Find clustering<br/>Path compression"):::key
    end

    subgraph stage2["Stage 2 — LLM Judge"]
        PROV("Build provenance map<br/>Entity to source text"):::process
        JUDGE("LLM Judge<br/>Merge / Separate decision"):::key
        CONV("cluster_to_entity<br/>Canonical name + synonyms"):::process
    end

    SING("Singletons<br/>Promote directly to Entity"):::process
    ENTS["Entity[]"]:::output

    TRIPS --> UNQ --> EMB --> SIM --> UF
    UF --> JUDGE
    PROV --> JUDGE
    JUDGE --> CONV --> ENTS
    UNQ -. "not in any cluster" .-> SING --> ENTS

    classDef input fill:#FAFAFA,stroke:#424242,stroke-width:2px
    classDef process fill:#F5F5F5,stroke:#9E9E9E,stroke-width:1.5px
    classDef key fill:#E3F2FD,stroke:#1565C0,stroke-width:2px,color:#0D47A1
    classDef output fill:#37474F,stroke:#263238,stroke-width:2px,color:#ECEFF1
```

---

## 09 - RAG Mapping + Validation

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#FAFAFA', 'primaryTextColor': '#212121', 'primaryBorderColor': '#9E9E9E', 'lineColor': '#616161', 'fontSize': '13px', 'fontFamily': 'Inter, Helvetica, Arial, sans-serif'}}}%%
flowchart TD
    TBL["EnrichedTableSchema"]:::input
    ENTS["Entity[]"]:::input

    subgraph retrieval["Retrieval Phase"]
        QRY("build_retrieval_query<br/>Table metadata to text"):::process
        RET("retrieve_top_entities<br/>Cosine similarity"):::process
    end

    subgraph generation["Generation Phase"]
        PROP("propose_mapping<br/>LLM + few-shot"):::key
        PVAL("Pydantic Validation<br/>Schema conformance"):::process
    end

    subgraph validation["Actor-Critic Validation"]
        CRIT("Critic Review<br/>LLM adversarial check"):::key
        BEST("Best-Proposal Tracking<br/>Highest confidence across retries"):::process
    end

    HITL("HITL Interrupt<br/>conf < threshold"):::optional
    REFL("Reflection injection<br/>Critique as context"):::process
    OUT["MappingProposal (validated)"]:::output

    TBL --> QRY
    ENTS --> RET
    QRY --> RET --> PROP
    PROP --> PVAL
    PVAL -- "error" --> REFL --> PROP
    PVAL -- "valid" --> CRIT
    CRIT -- "rejected" --> REFL
    CRIT -- "approved" --> BEST
    BEST -. "conf < gate" .-> HITL
    BEST -- "approved" --> OUT
    HITL --> OUT

    classDef input fill:#FAFAFA,stroke:#424242,stroke-width:2px
    classDef process fill:#F5F5F5,stroke:#9E9E9E,stroke-width:1.5px
    classDef key fill:#E3F2FD,stroke:#1565C0,stroke-width:2px,color:#0D47A1
    classDef optional fill:#FAFAFA,stroke:#9E9E9E,stroke-width:1.5px,stroke-dasharray: 5 5
    classDef output fill:#37474F,stroke:#263238,stroke-width:2px,color:#ECEFF1
```

---

## 10 - Graph Construction

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#FAFAFA', 'primaryTextColor': '#212121', 'primaryBorderColor': '#9E9E9E', 'lineColor': '#616161', 'fontSize': '13px', 'fontFamily': 'Inter, Helvetica, Arial, sans-serif'}}}%%
flowchart TD
    MAP["MappingProposal"]:::input

    subgraph gen["Cypher Generation"]
        FEW("Load few-shot examples<br/>few_shot_cypher.json"):::process
        GEN("generate_cypher<br/>LLM + CYPHER_SYSTEM prompt"):::key
    end

    subgraph heal["Self-Healing Loop"]
        VAL{"EXPLAIN<br/>dry-run"}:::gate
        FIX("fix_cypher<br/>LLM reflection on error"):::key
    end

    subgraph fallback["Deterministic Fallback"]
        DET("build_upsert_cypher<br/>Parametrized MERGE template"):::process
        FK("build_fk_cypher<br/>FK edge statements"):::process
    end

    NEO("Neo4j Upsert<br/>execute_cypher / execute_batch"):::process
    KG[("Neo4j<br/>Knowledge Graph")]:::database

    MAP --> FEW --> GEN
    GEN --> VAL
    VAL -- "valid" --> NEO
    VAL -- "syntax error" --> FIX --> VAL
    FIX -. "max attempts" .-> DET
    DET --> NEO
    FK --> NEO
    NEO --> KG

    classDef input fill:#FAFAFA,stroke:#424242,stroke-width:2px
    classDef process fill:#F5F5F5,stroke:#9E9E9E,stroke-width:1.5px
    classDef key fill:#E3F2FD,stroke:#1565C0,stroke-width:2px,color:#0D47A1
    classDef gate fill:#FAFAFA,stroke:#424242,stroke-width:2px
    classDef database fill:#37474F,stroke:#263238,stroke-width:2px,color:#ECEFF1
```

---

## 11 - Retrieval

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#FAFAFA', 'primaryTextColor': '#212121', 'primaryBorderColor': '#9E9E9E', 'lineColor': '#616161', 'fontSize': '13px', 'fontFamily': 'Inter, Helvetica, Arial, sans-serif'}}}%%
flowchart TD
    Q["Natural Language Query"]:::input

    subgraph channels["Parallel Retrieval Channels"]
        VEC("Vector Search<br/>BusinessConcept + Chunk embeddings"):::process
        BM25("BM25 Keyword Search<br/>In-memory index"):::process
        GRV("Graph Traversal<br/>Seed expansion via Cypher"):::process
        META("Structural Context<br/>FK rels + MAPPED_TO + all concepts"):::process
    end

    subgraph fusion["Fusion + Reranking"]
        MERGE("Merge Results<br/>Dedup by node_id, max score"):::process
        RERANK("Cross-Encoder Reranking<br/>bge-reranker-v2-m3"):::key
        FLOOR("Rank-based Confidence Floor<br/>Prevent low-score discard"):::process
    end

    OUT["RetrievedChunk[] (ranked)"]:::output

    Q --> VEC
    Q --> BM25
    Q --> GRV
    Q --> META
    VEC --> MERGE
    BM25 --> MERGE
    GRV --> MERGE
    META --> MERGE
    MERGE --> RERANK --> FLOOR --> OUT

    classDef input fill:#FAFAFA,stroke:#424242,stroke-width:2px
    classDef process fill:#F5F5F5,stroke:#9E9E9E,stroke-width:1.5px
    classDef key fill:#E3F2FD,stroke:#1565C0,stroke-width:2px,color:#0D47A1
    classDef output fill:#37474F,stroke:#263238,stroke-width:2px,color:#ECEFF1
```

---

## 12 - Answer Generation + Grading

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#FAFAFA', 'primaryTextColor': '#212121', 'primaryBorderColor': '#9E9E9E', 'lineColor': '#616161', 'fontSize': '13px', 'fontFamily': 'Inter, Helvetica, Arial, sans-serif'}}}%%
flowchart TD
    CHUNKS["Reranked Chunks"]:::input

    GATE{"Retrieval<br/>Quality Gate"}:::gate
    DIST("Context Distillation<br/>Noise removal + truncation"):::process
    COMP("Compose Generation Chunks<br/>Balanced source mix"):::process
    GEN("Answer Generation<br/>Context-adaptive prompt"):::key
    ABST("Abstention Correction<br/>Detect false abstentions"):::process
    GRAD("Hallucination Grader<br/>Self-RAG structured critique"):::key
    CONS("Grader Consistency Validator<br/>grounded vs action coherence"):::process
    FIN("Grounded Answer + Sources"):::output
    ABS("Abstain<br/>Insufficient context"):::optional

    CHUNKS --> GATE
    GATE -- "proceed" --> DIST
    GATE -. "abstain" .-> ABS
    DIST --> COMP --> GEN
    GEN --> ABST --> GRAD
    GRAD --> CONS
    CONS -- "pass" --> FIN
    CONS -- "regenerate" --> GEN

    classDef input fill:#FAFAFA,stroke:#424242,stroke-width:2px
    classDef process fill:#F5F5F5,stroke:#9E9E9E,stroke-width:1.5px
    classDef key fill:#E3F2FD,stroke:#1565C0,stroke-width:2px,color:#0D47A1
    classDef gate fill:#FAFAFA,stroke:#424242,stroke-width:2px
    classDef optional fill:#FAFAFA,stroke:#9E9E9E,stroke-width:1.5px,stroke-dasharray: 5 5
    classDef output fill:#37474F,stroke:#263238,stroke-width:2px,color:#ECEFF1
```

---

## 13 - REST API

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#FAFAFA', 'primaryTextColor': '#212121', 'primaryBorderColor': '#9E9E9E', 'lineColor': '#616161', 'fontSize': '13px', 'fontFamily': 'Inter, Helvetica, Arial, sans-serif'}}}%%
flowchart TD
    CLIENT["HTTP Client"]:::input

    AUTH("API Key Auth<br/>X-API-Key header"):::process

    subgraph demo["/api/v1/demo"]
        BUILD("POST /build<br/>Start KG construction"):::process
        QUERY("POST /query<br/>Synchronous Q&A"):::process
        PIPE("POST /pipeline<br/>E2E build + query"):::process
        STATS("GET /graph/stats<br/>Live KG statistics"):::process
    end

    subgraph ablation["/api/v1/ablation"]
        MATRIX("GET /matrix<br/>List 21 studies"):::process
        RUN("POST /run<br/>Launch ablation study"):::process
        STATUS("GET /status<br/>Poll job progress"):::process
    end

    JOBS("Job Store<br/>In-memory thread-safe"):::key
    BG("BackgroundTasks<br/>Async pipeline execution"):::process

    CLIENT --> AUTH
    AUTH --> demo
    AUTH --> ablation
    BUILD --> BG --> JOBS
    PIPE --> BG
    RUN --> BG

    classDef input fill:#FAFAFA,stroke:#424242,stroke-width:2px
    classDef process fill:#F5F5F5,stroke:#9E9E9E,stroke-width:1.5px
    classDef key fill:#E3F2FD,stroke:#1565C0,stroke-width:2px,color:#0D47A1
```

---

## 14 - Evaluation

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#FAFAFA', 'primaryTextColor': '#212121', 'primaryBorderColor': '#9E9E9E', 'lineColor': '#616161', 'fontSize': '13px', 'fontFamily': 'Inter, Helvetica, Arial, sans-serif'}}}%%
flowchart TD
    GOLD[("Gold Standard<br/>QA pairs JSON")]:::database
    KG[("Neo4j KG")]:::database

    LOAD("Gold Standard Loader<br/>Format normalization"):::process

    subgraph ragas["RAGAS Evaluation"]
        QG("Query Graph<br/>run_query per pair"):::process
        FAITH("Faithfulness"):::process
        REL("Answer Relevancy"):::process
        PREC("Context Precision"):::process
        REC("Context Recall"):::process
    end

    subgraph custom["Custom Metrics"]
        HEAL("Cypher Healing Rate"):::process
        HITL("HITL Confidence Agreement"):::process
    end

    BOOT("Bootstrap CI<br/>95% confidence intervals"):::key
    BUNDLE("Evaluation Bundle<br/>JSON artifact"):::key
    JUDGE("AI-as-Judge<br/>Qualitative assessment"):::key
    EXPORT("Thesis Export<br/>CSV + plots"):::output

    GOLD --> LOAD --> QG
    KG --> QG
    QG --> FAITH & REL & PREC & REC
    FAITH & REL & PREC & REC --> BOOT
    CUSTOM --> BOOT
    HEAL --> BOOT
    HITL --> BOOT
    BOOT --> BUNDLE --> JUDGE
    BUNDLE --> EXPORT

    classDef database fill:#37474F,stroke:#263238,stroke-width:2px,color:#ECEFF1
    classDef process fill:#F5F5F5,stroke:#9E9E9E,stroke-width:1.5px
    classDef key fill:#E3F2FD,stroke:#1565C0,stroke-width:2px,color:#0D47A1
    classDef output fill:#37474F,stroke:#263238,stroke-width:2px,color:#ECEFF1
```

---

## 15 - Ablation Framework

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#FAFAFA', 'primaryTextColor': '#212121', 'primaryBorderColor': '#9E9E9E', 'lineColor': '#616161', 'fontSize': '13px', 'fontFamily': 'Inter, Helvetica, Arial, sans-serif'}}}%%
flowchart TD
    MAT["ABLATION_MATRIX<br/>21 studies (AB-00..AB-20)"]:::input
    DS["7 Datasets<br/>(DS-01..DS-07)"]:::input

    OVR("_settings_override<br/>Context manager env injection"):::process
    BUILD("Builder Graph<br/>Construct KG"):::process
    QUERY("Query Graph<br/>Answer QA pairs"):::process
    RAGAS("RAGAS Metrics<br/>Per-question scores"):::key
    BW("Bundle Writer<br/>evaluation_bundle.json"):::process
    JUDGE("AI-as-Judge<br/>Qualitative rubric"):::key
    REPORT("Ablation Report<br/>Comparative statistics"):::output

    MAT --> OVR
    DS --> BUILD
    OVR --> BUILD --> QUERY --> RAGAS
    RAGAS --> BW --> JUDGE
    JUDGE --> REPORT

    classDef input fill:#FAFAFA,stroke:#424242,stroke-width:2px
    classDef process fill:#F5F5F5,stroke:#9E9E9E,stroke-width:1.5px
    classDef key fill:#E3F2FD,stroke:#1565C0,stroke-width:2px,color:#0D47A1
    classDef output fill:#37474F,stroke:#263238,stroke-width:2px,color:#ECEFF1
```
