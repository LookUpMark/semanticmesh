# Logging Strutturato e Pipeline Tracing

## 1. Panoramica Concettuale

Il sistema di osservabilità del progetto si articola su due livelli complementari:

1. **Logging strutturato JSON** (`src/config/logging.py`) — logging operativo in tempo reale, basato sulla libreria standard `logging` con formattazione JSON tramite `python-json-logger`. Ogni nodo LangGraph emette eventi strutturati con metadati standardizzati (durata, modello usato, conteggio token).

2. **Pipeline Tracing** (`src/config/tracing.py`) — trace end-to-end dell'intera esecuzione, che registra lo stato della pipeline a ogni fase (chunking, estrazione, entity resolution, mapping, Cypher, retrieval, generazione). I trace vengono salvati come file JSON/JSONL per analisi post-hoc e studi ablation.

Il logging risponde alla domanda *"cosa sta succedendo ora?"*, mentre il tracing risponde a *"cosa è successo nell'intera esecuzione e dove sono i bottleneck?"*.

## 2. Posizione nel Sistema

```
src/config/
├── logging.py   ← Logging JSON strutturato, helper per nodi LangGraph
└── tracing.py   ← BuilderTrace, QueryTrace, ComparisonReport
```

**Consumatori del logging:**

Tutti i moduli importano `get_logger(__name__)` e i helper `log_node_event()` / `log_retry_event()`:

```python
from src.config.logging import get_logger, log_node_event, log_retry_event
logger = get_logger(__name__)
```

**Consumatori del tracing:**

- `src/graph/builder_graph.py` → crea e popola `BuilderTrace` in `run_builder()`
- `src/generation/query_graph.py` → crea e popola `QueryTrace` in `run_query()`
- `src/evaluation/ablation_runner.py` → abilita il tracing negli esperimenti
- Notebook di analisi → caricano e analizzano i trace JSON

## 3. Stato dell'Arte e Letteratura

- **Structured Logging** (12-Factor App, requisito XI — Log): i log devono essere stream di eventi strutturati, non file di testo. La formattazione JSON permette parsing automatico e integrazione con sistemi di aggregazione (ELK, Datadog, CloudWatch).
- **python-json-logger** (2024): libreria leggera che estende `logging.Formatter` per emettere JSON con campi rinominabili e custom fields via `extra`.
- **Distributed Tracing** (OpenTelemetry, 2024): paradigma di tracciamento distribuito con span, trace ID e correlazione. Il sistema implementa un subset semplificato adatto a pipeline single-process.
- **LangSmith Tracing** (LangChain, 2024): tracing nativo integrato nella catena LangChain, abilitabile via variabile d'ambiente. Complementare al sistema custom.
- **Observability-Driven Development**: la pratica di progettare i sistemi con osservabilità incorporata (non aggiunta a posteriori), evidenziata dal pattern `log_node_event()` chiamato alla fine di ogni nodo.

## 4. Architettura Dettagliata

### 4.1 Logging Strutturato (`logging.py`)

#### Configurazione Root Logger

Al momento dell'importazione del modulo, `_configure_root_logger()` viene eseguito automaticamente:

```python
def _configure_root_logger() -> None:
    root = logging.getLogger()
    if root.handlers:
        return  # Già configurato, evita duplicazioni

    level_name = os.environ.get("LOG_LEVEL", "INFO").upper()
    root.setLevel(level)

    handler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter(
        fmt="%(asctime)s %(name)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
        rename_fields={"asctime": "ts", "name": "logger", "levelname": "level"},
    )
    handler.setFormatter(formatter)
    root.addHandler(handler)
```

L'output è JSON one-line:

```json
{"ts": "2024-12-15T10:32:45", "logger": "src.extraction.triplet_extractor", "level": "INFO", "message": "node_event", "node_name": "extract_triplets", "duration_ms": 1234.56}
```

I campi standard vengono rinominati: `asctime→ts`, `name→logger`, `levelname→level`. Il logger `neo4j.notifications` è silenziato a WARNING per evitare rumore.

#### Notebook Formatter

Per uso interattivo in Jupyter, `setup_notebook_logging()` sostituisce il formatter JSON con uno compatto human-readable:

```python
class _NotebookFormatter(logging.Formatter):
    def format(self, record):
        # Output: "HH:MM:SS  logger.name                  message"
        # Warning: "HH:MM:SS  [WARN]  logger.name          warning message"
```

Sopprime i logger rumorosi di terze parti (`httpx`, `httpcore`, `urllib3`, `pydantic`, `openai`, `anthropic`, etc.) e l'output di `transformers`.

#### `get_logger(name)`

```python
def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
```

Funzione wrapper semplice che restituisce un logger standard Python. Il nome convenzionale è `__name__` del modulo chiamante, producendo una gerarchia `src.extraction.triplet_extractor`.

#### `NodeTimer` — Context Manager

```python
class NodeTimer:
    """Context manager per misurare la durata di un blocco di codice."""
    def __enter__(self): ...
    def __exit__(self, ...): ...
    @property
    def elapsed_ms(self) -> float: ...
```

Usato sia nei nodi LangGraph che in `InstrumentedLLM`:

```python
with NodeTimer() as t:
    response = self._model.invoke(input)
self._log_call(response, elapsed_ms=t.elapsed_ms)
```

#### `log_node_event()` — Evento di Nodo

```python
def log_node_event(
    logger: logging.Logger,
    node_name: str,
    input_summary: str,
    output_summary: str,
    duration_ms: float,
    model_used: str = "",
    **extra: Any,
) -> None:
```

**Convenzione**: chiamare alla **fine** di ogni nodo LangGraph. Emette un log INFO con metadati strutturati:

```json
{
    "ts": "...", "level": "INFO", "message": "node_event",
    "node_name": "extract_triplets",
    "input_summary": "12 chunks",
    "output_summary": "47 triplets extracted",
    "duration_ms": 5432.10,
    "model_used": "gpt-5.4-nano"
}
```

#### `log_retry_event()` — Evento di Retry

```python
def log_retry_event(
    logger: logging.Logger,
    node_name: str,
    attempt_number: int,
    error_injected: str,
    correction_applied: str = "",
) -> None:
```

**Convenzione**: chiamare all'**inizio** di ogni iterazione di retry (Actor-Critic, Cypher Healing, Hallucination Grading). Emette un log WARNING:

```json
{
    "ts": "...", "level": "WARNING", "message": "retry_event",
    "node_name": "validate_mapping",
    "attempt_number": 2,
    "error_injected": "Concept 'CUST_ID' not found in entity context"
}
```

#### Suppressione Warning Import-Time

```python
warnings.filterwarnings("ignore", message="IProgress not found", category=UserWarning)
warnings.filterwarnings("ignore", message="directory.*does not exist", category=UserWarning)
```

Elimina i warning rumorosi di tqdm/IProgress e directory cache all'import di librerie ML.

### 4.2 Pipeline Tracing (`tracing.py`)

#### Costanti Globali

```python
TRUNCATE_LENGTH = 500  # Max lunghezza testo nei trace
MAX_ITEMS = 100        # Max elementi per lista nei trace
```

Le funzioni `truncate_text()` e `truncate_list()` prevengono trace JSON troppo grandi, aggiungendo marker `[TRUNCATED]` quando necessario.

#### `BuilderTrace` — Trace del Builder Graph

Dataclass che registra l'intera esecuzione del Builder:

```python
@dataclass
class BuilderTrace:
    # Metadata
    study_id: str          # es. "AB-00"
    timestamp: str         # ISO 8601
    trace_id: str          # auto-generato: "{study_id}.{timestamp}"
    config: dict           # Snapshot della configurazione usata

    # Input
    source_documents: list[str]
    ddl_files: list[str]

    # Per-stage records
    chunks: list[dict]                   # Chunking
    triplets: list[dict]                 # Estrazione
    entities_pre_resolution: list[dict]  # Pre-ER
    blocks: list[dict]                   # Blocking K-NN
    cluster_decisions: list[dict]        # Decisioni LLM judge
    entities_post_resolution: list[dict] # Post-ER
    tables_parsed: list[dict]            # DDL parsing
    tables_enriched: list[dict]          # Schema enrichment
    table_mappings: list[dict]           # Mapping
    cypher_queries: list[dict]           # Cypher gen + healing
    neo4j_summary: dict                  # Statistiche Neo4j finali

    # Timing
    stage_timings: dict[str, float]
```

**Metodi principali:**

| Metodo | Fase | Dati Registrati |
|--------|------|-----------------|
| `create()` | Init | `study_id`, snapshot settings, file path input |
| `record_chunks()` | Chunking | Chunk con testo troncato, conteggio token, summary |
| `record_triplets()` | Estrazione | Triplet (S,P,O) con confidence, summary |
| `record_entity_resolution()` | ER | Entità pre/post, blocchi, decisioni judge, reduction rate |
| `record_schema_processing()` | DDL+Enrichment | Tabelle parsate, descrizioni arricchite |
| `record_mapping()` | Mapping | Mapping table→concept con confidence, alternative |
| `record_cypher_and_graph()` | Cypher+Neo4j | Query Cypher, successo/fallimento, healing attempts |
| `save()` | Fine | Salvataggio JSON singolo in `output_dir/` |

Il `trace_id` è auto-generato come `"{study_id}.{timestamp}"` nel `__post_init__`.

#### `QueryTrace` — Trace del Query Graph

Dataclass che registra una singola esecuzione Query:

```python
@dataclass
class QueryTrace:
    # Metadata
    study_id: str
    question: str
    trace_id: str           # auto: "{study_id}.Q{index}.{timestamp}"
    builder_trace_id: str   # Collegamento al BuilderTrace associato
    query_index: int

    # Per-stage records
    vector_results: list[dict]          # Risultati vector search
    bm25_results: list[dict]            # Risultati BM25
    graph_traversal_results: list[dict] # Risultati graph traversal
    rrf_fused: list[dict]               # Risultati dopo RRF fusion
    pre_rerank: list[dict]              # Pre cross-encoder
    post_rerank: list[dict]             # Post cross-encoder (con score delta)
    contexts_for_generation: list[dict] # Contesti finali per LLM
    generation_attempts: list[dict]     # Ogni tentativo con answer, critique, decision

    # Output
    final_answer: str
    grounded: bool
    verification_score: float
    sources: list[str]
```

**Metodi principali:**

| Metodo | Fase | Dati Registrati |
|--------|------|-----------------|
| `create()` | Init | question, query_index, collegamento a builder_trace |
| `record_retrieval()` | Retrieval | Risultati vector, BM25, graph, RRF con score |
| `record_reranking()` | Reranking | Pre/post rerank con score delta e rank change |
| `record_context_preparation()` | Distillazione | Contesti selezionati, totale caratteri |
| `record_generation_attempt()` | Generazione | Answer, critique, grader decision per tentativo |
| `record_output()` | Fine | Risposta finale, groundedness, verification score |
| `save()` | Fine | Append JSONL in file condiviso |

**Nota**: a differenza di `BuilderTrace` che salva un JSON singolo, `QueryTrace` usa **JSONL** (una riga JSON per query) per aggregare più query nello stesso file.

#### `ComparisonReport` — Analisi Trace vs Ground Truth

Dataclass per confrontare i risultati del retrieval con le sorgenti attese (gold standard):

```python
@dataclass
class ComparisonReport:
    study_id: str
    per_question_analysis: list[dict]  # Coverage per domanda
    aggregate_metrics: dict            # Metriche aggregate
    bottlenecks: list[dict]            # Colli di bottiglia identificati
    recommendations: list[str]         # Raccomandazioni automatiche
```

**Workflow di analisi:**

1. `generate_per_question_analysis(query_traces, ground_truth)` — confronta le sorgenti recuperate con quelle attese, calcola coverage rate.
2. `generate_aggregate_metrics()` — media coverage, grounding rate, verification score.
3. `identify_bottlenecks()` — identifica problemi (bassa coverage, basso grounding) con severità.
4. `generate_recommendations()` — suggerimenti automatici (aumentare top-K, rivedere prompt, etc.).
5. `to_markdown()` → `save()` — report Markdown con tabella per-question.

## 5. Implementazione nel Codice

### 5.1 Integrazione nel Builder Graph

In `run_builder()` (`src/graph/builder_graph.py`):

```python
# Creazione trace
if trace_enabled:
    builder_trace = BuilderTrace.create(
        study_id=study_id, settings=settings,
        doc_paths=doc_paths, ddl_paths=ddl_path_objs,
    )
    builder_trace.record_chunks(chunk_dicts)

# Lo stato iniziale porta il trace nel grafo
initial: BuilderState = {
    "trace_enabled": trace_enabled,
    "builder_trace": builder_trace,
    ...
}

# Dopo graph.invoke(), popolazione finale
final_state = graph.invoke(initial, config=config)

if trace_enabled and builder_trace:
    builder_trace.record_triplets(triplet_dicts)
    builder_trace.entities_post_resolution = entity_dicts
    builder_trace.record_schema_processing(table_dicts, enriched_table_dicts)
    # Statistiche Neo4j
    with Neo4jClient() as client:
        node_count = client.execute_cypher("MATCH (n) RETURN count(n) as count")[0]["count"]
        builder_trace.neo4j_summary = {"total_nodes": node_count, ...}
    # Salvataggio DOPO la popolazione completa
    trace_path = builder_trace.save(output_dir)
```

**Pattern chiave**: il trace viene salvato **dopo** `graph.invoke()`, non durante — questo evita timing bug in cui il trace viene scritto prima che tutti i dati siano disponibili.

### 5.2 Integrazione nel Query Graph

In `run_query()` (`src/generation/query_graph.py`):

```python
if trace_enabled:
    query_trace = QueryTrace.create(
        study_id=study_id, question=user_query,
        query_index=query_index, builder_trace_id=builder_trace_id,
    )

final_state = graph.invoke(initial, config=config)

# Salvataggio trace (JSONL append)
if trace_enabled and query_trace:
    query_trace.record_output(...)
    query_trace.save(output_file)
```

### 5.3 Logging in InstrumentedLLM

Ogni invocazione LLM emette un log strutturato:

```python
class InstrumentedLLM:
    def _log_call(self, response, *, elapsed_ms, attempt):
        usage = getattr(response, "usage_metadata", {})
        self._logger.info(
            "llm.%s call completed | attempt=%d | latency_ms=%.1f | "
            "input_tokens=%s | output_tokens=%s | total_tokens=%s",
            self._name, attempt, elapsed_ms,
            usage.get("input_tokens", "?"),
            usage.get("output_tokens", "?"),
            usage.get("total_tokens", "?"),
        )
```

## 6. Flusso dei Dati

### 6.1 Logging

```
Nodo LangGraph
    │
    ├── get_logger(__name__) ── logger "src.graph.build_nodes"
    │
    ├── [Esecuzione logica]
    │
    ├── log_retry_event(...)   ← Se in loop di retry (inizio iterazione)
    │
    └── log_node_event(...)    ← Fine nodo (sempre)
            │
            ▼
    Root Logger (JSON formatter)
            │
            ▼
    StreamHandler → stderr
            │
            ▼
    {"ts": "...", "level": "INFO", "node_name": "build_graph", ...}
```

### 6.2 Tracing

```
run_builder()                           run_query()
     │                                       │
     ▼                                       ▼
BuilderTrace.create()                  QueryTrace.create()
     │                                       │
     ▼                                       ▼
record_chunks()                        [graph.invoke()]
     │                                       │
     ▼                                       ▼
[graph.invoke()]                       record_retrieval()
     │                                 record_reranking()
     ▼                                 record_context_preparation()
record_triplets()                      record_generation_attempt() × N
record_entity_resolution()             record_output()
record_schema_processing()                   │
record_mapping()                             ▼
record_cypher_and_graph()              query_trace.save()
     │                                       │
     ▼                                       ▼
builder_trace.save()                   output.jsonl (JSONL append)
     │
     ▼
builder_trace_{id}.json (JSON singolo)
```

## 7. Configurazione e Parametri

### 7.1 Parametri Logging

| Parametro | Sorgente | Default | Descrizione |
|-----------|----------|---------|-------------|
| `LOG_LEVEL` | Env var | `"INFO"` | Livello root logger |
| N/A | `setup_notebook_logging()` | — | Abilita formato human-readable |

### 7.2 Parametri Tracing

| Parametro | Config Field | Default | Descrizione |
|-----------|-------------|---------|-------------|
| `enable_debug_trace` | `settings.enable_debug_trace` | `False` | Abilita trace system globalmente |
| `trace_output_dir` | `settings.trace_output_dir` | `"notebooks/ablation/ablation_results/traces/debug"` | Directory output trace |
| `trace_compress_large_fields` | `settings.trace_compress_large_fields` | `True` | Abilita troncamento campi grandi |
| `trace_truncate_length` | `settings.trace_truncate_length` | `500` | Lunghezza max testo nei trace |
| `trace_max_items` | `settings.trace_max_items` | `100` | Elementi max per lista nei trace |

### 7.3 Parametri per `run_builder()` / `run_query()`

| Parametro | Tipo | Descrizione |
|-----------|------|-------------|
| `trace_enabled` | `bool` | Abilita tracing per questa esecuzione |
| `study_id` | `str` | Identificativo studio (es. "AB-00") per naming dei file |
| `builder_trace_id` | `str` | (solo query) Collegamento al builder trace associato |
| `query_index` | `int` | (solo query) Indice nella batch di query |

## 8. Testing e Verifica

### 8.1 Test del Logging

```python
def test_get_logger_returns_named_logger():
    logger = get_logger("test.module")
    assert logger.name == "test.module"

def test_log_node_event_emits_info(caplog):
    logger = get_logger("test")
    with caplog.at_level(logging.INFO):
        log_node_event(logger, "test_node", "input", "output", 100.0)
    assert "node_event" in caplog.text

def test_log_retry_event_emits_warning(caplog):
    logger = get_logger("test")
    with caplog.at_level(logging.WARNING):
        log_retry_event(logger, "test_node", 2, "error msg")
    assert "retry_event" in caplog.text
```

### 8.2 Test del Tracing

```python
def test_builder_trace_create():
    trace = BuilderTrace.create(study_id="TEST-01")
    assert trace.study_id == "TEST-01"
    assert trace.trace_id.startswith("TEST-01.")

def test_builder_trace_record_chunks():
    trace = BuilderTrace.create(study_id="TEST")
    chunks = [{"chunk_id": 0, "text": "Long " * 200, "token_count": 50}]
    trace.record_chunks(chunks)
    assert len(trace.chunks) == 1
    assert trace.chunks[0]["text"].endswith("[TRUNCATED]")
    assert trace.chunking_summary["total_chunks"] == 1

def test_query_trace_saves_jsonl(tmp_path):
    trace = QueryTrace.create(study_id="TEST", question="Q?", query_index=0)
    trace.record_output("Answer", grounded=True, verification_score=0.9, ...)
    output_file = tmp_path / "traces.jsonl"
    trace.save(output_file)
    lines = output_file.read_text().strip().split("\n")
    assert len(lines) == 1
    data = json.loads(lines[0])
    assert data["question"] == "Q?"

def test_truncate_text():
    assert truncate_text("short") == "short"
    long_text = "x" * 1000
    result = truncate_text(long_text, max_length=500)
    assert result.endswith("[TRUNCATED]")
    assert len(result) < 520
```

### 8.3 Comandi

```bash
pytest tests/unit/ -k "logging or tracing" -v
ruff check src/config/logging.py src/config/tracing.py
```

## 9. Note di Manutenzione ed Estensione

### 9.1 Aggiungere una Nuova Fase al Trace

Per registrare una nuova fase nel `BuilderTrace`:

1. Aggiungere i campi `dataclass` (es. `new_phase: list[dict]`, `new_phase_summary: dict`).
2. Implementare `record_new_phase()` con troncamento appropriato.
3. Chiamare il metodo in `run_builder()` dopo `graph.invoke()`.
4. I file trace esistenti restano compatibili: i nuovi campi avranno valori default.

### 9.2 Integrazione con Sistemi Esterni

Il formato JSON strutturato del logging si presta all'integrazione con:

- **ELK Stack**: configurare Filebeat per raccogliere l'output JSON da stderr.
- **Datadog/CloudWatch**: aggiungere handler custom che invii gli eventi.
- **Grafana+Loki**: il formato one-line JSON è direttamente indicizzabile.

Per LangSmith, basta impostare:

```bash
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_API_KEY=ls-...
```

Il tracing LangSmith è ortogonale al sistema custom: registra automaticamente tutte le chiamate LangChain senza modifiche al codice.

Per Langfuse, impostare:

```bash
export LANGFUSE_PUBLIC_KEY=pk-lf-...
export LANGFUSE_SECRET_KEY=sk-lf-...
export LANGFUSE_HOST=https://cloud.langfuse.com
```

Langfuse viene iniettato come `LangchainCallbackHandler` in ogni chiamata LLM tramite `InstrumentedLLM._inject_observability_callbacks()`. Il modulo `src/config/observability.py` gestisce il lifecycle dei callback handler (creazione lazy con `@lru_cache`, flush allo shutdown, reset dopo cambio env vars).

Entrambi sono opzionali e possono coesistere: LangSmith opera via hook interni di LangChain (nessun callback esplicito), Langfuse opera via callback handler esplicito passato a `model.invoke(config={"callbacks": [...]})`.

**File chiave**: `src/config/observability.py` — funzioni esportate:
- `get_observability_callbacks()` → lista di handler attivi (Langfuse se configurato)
- `is_langsmith_enabled()` / `is_langfuse_enabled()` → check di stato
- `flush_observability()` → flush pending data (chiamato da FastAPI shutdown)
- `reset_observability()` → clear cache (dopo modifica env vars)

### 9.3 Performance Considerations

- **Troncamento**: `TRUNCATE_LENGTH=500` e `MAX_ITEMS=100` sono scelti per bilanciare dettaglio e dimensione dei file. Per debug approfonditi, aumentare temporaneamente.
- **Salvataggio**: `BuilderTrace.save()` scrive un file JSON per esecuzione. `QueryTrace.save()` usa JSONL append, ottimale per batch di query.
- **Overhead**: il logging JSON aggiunge ~5 μs per evento. Il tracing è solo attivo quando `trace_enabled=True`.

### 9.4 Attenzione

- **`setup_notebook_logging()`** va chiamata **una volta** dopo `reconfigure_from_env()` nel notebook — chiamarla più volte non duplica gli handler (li rimuove e ricrea).
- **`_configure_root_logger()`** ha un guard `if root.handlers: return` per evitare duplicazione se il modulo viene re-importato. Non rimuovere questo guard.
- Il **`ComparisonReport`** richiede un `gold_standard.json` con campo `expected_sources` per funzionare — senza di esso, il coverage è sempre 100%.
- I trace JSONL (`QueryTrace.save()`) usano **append mode**: per un nuovo esperimento, eliminare o rinominare il file precedente.

## 10. Riferimenti

### File Sorgente
- [src/config/logging.py](../../src/config/logging.py) — Logging JSON strutturato
- [src/config/tracing.py](../../src/config/tracing.py) — BuilderTrace, QueryTrace, ComparisonReport
- [src/config/observability.py](../../src/config/observability.py) — LangSmith + Langfuse callback management

### File Correlati
- [src/graph/builder_graph.py](../../src/graph/builder_graph.py) — Integrazione trace nel Builder
- [src/generation/query_graph.py](../../src/generation/query_graph.py) — Integrazione trace nel Query
- [src/config/llm_client.py](../../src/config/llm_client.py) — Logging in InstrumentedLLM (NodeTimer)

### Documentazione
- [SPECS.md](../draft/SPECS.md) — Specifiche architetturali
- [01-settings.md](01-settings.md) — Parametri di configurazione
- [02-llm-factory.md](02-llm-factory.md) — LLM Factory e InstrumentedLLM

### Letteratura
- Wiggins, A. (2011). *The Twelve-Factor App* — Requisito XI: Logs. https://12factor.net/logs
- OpenTelemetry (2024). *Observability Primer*. https://opentelemetry.io/docs/concepts/
- python-json-logger (2024). *JSON Logging for Python*. https://github.com/madzak/python-json-logger
- LangChain (2024). *LangSmith Tracing*. Documentation.
