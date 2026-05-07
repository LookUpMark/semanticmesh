# Orchestrazione del Builder Graph

## 1. Panoramica Concettuale

Il Builder Graph e il primo dei due grafi LangGraph del sistema e implementa l'intera pipeline di costruzione della Knowledge Graph. Orchestrando nove nodi sequenziali e condizionali, trasforma documenti PDF non strutturati e schemi DDL relazionali in un grafo semantico su Neo4j, composto da:

- **BusinessConcept** -- Entita business estratte dai documenti (es. "Customer", "Product")
- **PhysicalTable** -- Tabelle fisiche dal DDL con metadati delle colonne
- **MAPPED_TO** -- Relazione tra concetto business e tabella fisica
- **REFERENCES** -- Relazioni FK tra tabelle fisiche
- **MENTIONS** -- Collegamenti tra chunk documentali e concetti
- **ParentChunk / Chunk** -- Chunk gerarchici con embedding vettoriale

La pipeline e interamente idempotente: esecuzioni ripetute non duplicano dati grazie all'uso esclusivo di `MERGE`.

### File coinvolti

| File | Responsabilita |
|------|---------------|
| `src/graph/builder_graph.py` | Definizione nodi, factory del grafo, entry point `run_builder()` |
| `src/graph/parallel_mapping.py` | ThreadPool per mapping+validation parallelo su tutte le tabelle |
| `src/graph/build_nodes.py` | Nodi di generazione Cypher, healing e scrittura su Neo4j |
| `src/graph/validation_nodes.py` | Validazione Actor-Critic con best-proposal tracking |

## 2. Posizione nel Sistema

Il Builder Graph corrisponde agli epic EP-01 fino a EP-11 del sistema. E invocato tramite `run_builder()` ed e il grafo "scrittore": costruisce il Knowledge Graph che il Query Graph (EP-12 fino a EP-15) poi interroga.

```
PDF documents + DDL files
        |
        v
   run_builder()
        |
        v
[load_pdf -> chunk -> persist chunks with embeddings]
        |
        v
Builder StateGraph:
  extract_triplets --> entity_resolution --> parse_ddl --> enrich_schema
       --> parallel_mapping --> rag_mapping --> validate_mapping --> [hitl]
       --> generate_cypher --> heal_cypher --> build_graph
       --> [loop: rag_mapping | save_trace]
```

## 3. Stato dell'Arte e Letteratura

### LangGraph e workflow orchestration
LangGraph (LangChain, 2024) estende LangChain con un modello a state graph basato su `StateGraph` con nodi e archi condizionali. Ogni nodo riceve lo stato completo (`TypedDict`) e ritorna un dizionario parziale di aggiornamento. Questo pattern e preferito rispetto a catene lineari per pipeline complesse con branching e cicli.

### LangGraph Studio
Il file `langgraph.json` nella root del progetto configura il grafo per LangGraph Studio (IDE visuale), registrando i due grafi (`builder` → `build_builder_graph`, `query` → `build_query_graph`) con riferimento ai rispettivi file sorgente.

### Graph-based agent architectures
L'architettura multi-agente basata su grafi di stato e un paradigma emergente in cui ogni nodo del grafo incapsula un'agente specializzato (es. estrazione, risoluzione, validazione). Il routing condizionale permette iterazioni self-correcting senza loop infiniti, grazie a contatori di tentativi e soglie.

### Checkpointing (MemorySaver / SqliteSaver)
LangGraph supporta checkpoint automatici dello stato tra i nodi. `MemorySaver` e in-process ed effimero (sviluppo), mentre `SqliteSaver` persiste su disco (produzione). Il checkpointing abilita l'interruzione e ripresa (`interrupt_before`) per Human-in-the-Loop.

### Conditional routing
Gli archi condizionali (`add_conditional_edges`) permettono routing basato sullo stato: una funzione predicato ispeziona lo stato corrente e ritorna il nome del nodo successivo. Questo e fondamentale per i cicli di reflection (validation -> rag_mapping -> validation) e per il branching HITL.

## 4. Architettura Dettagliata

### 4.1 Nodi in `builder_graph.py`

**`_node_extract_triplets(state)`** (EP-03)
Se `use_lazy_extraction` e attivo, usa `extract_all_triplets_heuristic()` (spaCy). Altrimenti, ottiene `get_extraction_llm()` e chiama `extract_all_triplets()`. Ritorna `{"triplets": [...]}`.

**`_node_entity_resolution(state)`** (EP-04)
Ottiene `get_embeddings()` e `get_lightweight_llm()`, chiama `resolve_entities()` con i triplet e il documento sorgente. Ritorna `{"entities": [...]}`.

**`_node_parse_ddl(state)`** (EP-05)
Itera sui percorsi DDL in `state["ddl_paths"]`, chiama `parse_ddl_file()` per ciascuno. Ritorna `{"tables": [...]}`.

**`_node_enrich_schema(state)`** (EP-05)
Se `enable_schema_enrichment` e `False`, promuove i `TableSchema` a `EnrichedTableSchema` senza arricchimento. Altrimenti, chiama `enrich_all()` con il lightweight LLM per espansione acronimi e descrizioni.

**`_node_parallel_mapping(state)`** (EP-06, Performance)
Quando `mapping_concurrency > 1`, processa tutte le tabelle in parallelo attraverso il loop mapping+validation usando `ThreadPoolExecutor`. Le proposte validate vengono archiviate in `precomputed_proposals` nello stato. I successivi nodi `rag_mapping` e `validate_mapping` le consumano senza ripetere chiamate LLM. Quando `mapping_concurrency == 1`, e un pass-through no-op.

**`_node_rag_mapping(state)`** (EP-06, EP-07)
Gestisce una coda di tabelle (`pending_tables`). Per ogni tabella:
1. Costruisce la query di retrieval via `build_retrieval_query()`
2. Recupera le top entita via `retrieve_top_entities()`
3. Se reflection: inietta il critique nel prompt di mapping
4. Chiama `propose_mapping()` o `propose_mapping_heuristic()` (lazy mode)
Ritorna `{"mapping_proposal", "current_table", "current_entities", "pending_tables", ...}`.

**`_route_after_build(state)`**
Se ci sono tabelle rimanenti in `pending_tables`, ritorna `"rag_mapping"`. Altrimenti ritorna `"save_trace"`.

**`_node_save_trace(state)`**
No-op: il trace viene salvato dopo `graph.invoke()` in `run_builder()`, quando lo stato e completo.

### 4.2 Nodi in `build_nodes.py`

**`_node_generate_cypher(state)`**
Se lazy mode, salta e ritorna `{"current_cypher": None}`. Altrimenti:
1. Ottiene `get_reasoning_llm()`
2. Trova l'entita risolta corrispondente al concetto mappato
3. Carica few-shot examples via `load_cypher_examples()`
4. Chiama `generate_cypher()` (modulo `cypher_generator.py`)

**`_node_heal_cypher(state)`**
Se lazy mode o `enable_cypher_healing` e `False`, ritorna `{"cypher_failed": True}`. Altrimenti esegue `heal_cypher()` con il driver Neo4j.

**`_node_build_graph(state)`** (EP-09, EP-10)
Strategia primary/fallback:
1. Se `current_cypher` valido e `cypher_failed=False`: esegue Cypher LLM
2. Altrimenti: chiama `build_upsert_cypher()` (builder deterministico)
3. Normalizza `PhysicalTable.table_name` in maiuscolo
4. Crea archi FK via `build_fk_cypher()`
5. Assegna embedding al `BusinessConcept` via `embed_text()`
6. Crea archi `MENTIONS` (chunk -> concept) basandosi sui triplet
7. Aggiorna `completed_tables`

**`_route_after_heal(state)`**
Ritorna sempre `"build_graph"` -- la strategia primary/fallback e gestita internamente da `_node_build_graph`.

### 4.3 Nodi in `validation_nodes.py`

**`_node_validate_mapping(state)`** (EP-08)
Validazione a due strati con best-proposal tracking:
1. **Layer 1 -- Pydantic**: `validate_schema()` verifica conformita allo schema
2. **Layer 2 -- LLM Critic**: `critic_review()` valuta la qualita del mapping (se `enable_critic_validation`)
3. Se il critic rifiuta e ci sono tentativi rimanenti, genera un `reflection_prompt` per ritentare
4. Se il critic rifiuta dopo `max_reflection_attempts`, accetta il `best_proposal` (massima confidence)
5. Se la confidence e sotto soglia, setta `hitl_flag=True`

**`_route_after_validate(state)`**
- Se `hitl_flag` e non `skip_hitl`: ritorna `"hitl"`
- Se `reflection_prompt` presente: ritorna `"rag_mapping"` (ciclo di reflection)
- Altrimenti: `"generate_cypher"` (normale) o `"build_graph"` (lazy)

### 4.4 Factory: `build_builder_graph()`

```python
def build_builder_graph(*, production=False):
    graph = StateGraph(BuilderState)
    # 10 nodi registrati
    # Entry: "extract_triplets"
    # Edge lineari: extract -> resolution -> parse -> enrich -> rag_mapping
    #              rag_mapping -> validate -> [condizionale] -> ...
    #              hitl -> generate_cypher -> heal_cypher
    # Edge condizionali: validate -> {hitl, rag_mapping, generate_cypher, build_graph}
    #                    heal -> build_graph
    #                    build -> {rag_mapping, save_trace}
    # Checkpointer: MemorySaver (default) o SqliteSaver (production)
    # interrupt_before: ["hitl"] se production
    return graph.compile(checkpointer=..., interrupt_before=...)
```

### 4.5 Entry point: `run_builder()`

```python
def run_builder(raw_documents, ddl_paths, *, production=False, clear_graph=False,
                use_lazy_extraction=None, trace_enabled=False, study_id="manual"):
```

1. Carica tutti i PDF con `load_pdf()` e chunk con `chunk_documents_hierarchical()`
2. Inizializza `BuilderTrace` se `trace_enabled`
3. Apre `Neo4jClient`, esegue `setup_schema()`, opzionalmente pulisce il grafo
4. Persiste `ParentChunk` (senza embedding) e `Chunk` (con embedding) su Neo4j
5. Crea archi `CHILD_OF` tra chunk e parent
6. Compila il grafo e invoca con stato iniziale
7. Popola e salva il trace se abilitato

## 5. Implementazione nel Codice

### `src/graph/builder_graph.py` (righe 1-483)

Il file contiene:
- 6 implementazioni di nodi (righe 54-160)
- 1 predicato di routing (righe 168-173)
- 1 nodo trace no-op (righe 181-188)
- `build_builder_graph()` (righe 196-269)
- `run_builder()` (righe 272-483)

### `src/graph/build_nodes.py` (righe 1-227)

Contiene 4 nodi (`_node_generate_cypher`, `_node_heal_cypher`, `_node_build_graph`, `_route_after_heal`) piu la helper `_find_entity_for_concept` (lookup case-insensitive).

### `src/graph/validation_nodes.py` (righe 1-120)

Contiene `_node_validate_mapping` con best-proposal tracking e `_route_after_validate` con routing condizionale.

## 6. Flusso dei Dati

```
run_builder(raw_documents, ddl_paths)
  |
  +-- load_pdf() -> Document[]
  +-- chunk_documents_hierarchical() -> (parents[], children[])
  +-- Neo4jClient: persist ParentChunk, Chunk, CHILD_OF edges
  |
  v
Builder StateGraph.invoke({
  chunks: parents,
  ddl_paths: [...],
  source_doc: "...",
  use_lazy_extraction: bool,
  ...
})
  |
  v
extract_triplets:
  chunks -> [Triplet{subject, predicate, object, confidence, source_chunk_index}]
  |
  v
entity_resolution:
  triplets -> [Entity{name, definition, synonyms, provenance_text, source_doc}]
  |
  v
parse_ddl:
  ddl_paths -> [TableSchema{table_name, columns[], ddl_source}]
  |
  v
enrich_schema:
  tables -> [EnrichedTableSchema{table_name, columns[], table_description, ...}]
  |
  v
rag_mapping (per tabella):
  enriched_tables (coda) + entities -> MappingProposal{mapped_concept, confidence, reasoning}
  |
  v
validate_mapping:
  proposal -> Pydantic check -> Critic review -> {accept, retry, hitl}
  |
  v
[hitl: interrupt() -> resume con feedback umano]
  |
  v
generate_cypher:
  mapping + table + entity -> stringa Cypher
  |
  v
heal_cypher:
  cypher -> EXPLAIN -> (valid | fix + retry | None)
  |
  v
build_graph:
  Cypher validato/deterministico -> MERGE su Neo4j
  + FK edges, embedding, MENTIONS edges
  |
  v
[loop: rag_mapping per prossima tabella | save_trace -> END]
```

## 7. Configurazione e Parametri

| Parametro | Default | Descrizione |
|-----------|---------|-------------|
| `enable_schema_enrichment` | `True` | Salta espansione acronimi se `False` |
| `enable_cypher_healing` | `True` | Salta healing se `False` |
| `enable_critic_validation` | `True` | Salta validazione Actor-Critic se `False` |
| `confidence_threshold` | 0.90 | Soglia per attivare HITL |
| `max_reflection_attempts` | 3 | Max tentativi per reflection Actor-Critic |
| `max_cypher_healing_attempts` | 3 | Max tentativi per healing Cypher |
| `use_lazy_extraction` | `False` | Usa estrazione euristica invece di LLM |
| `sqlite_checkpoint_path` | variabile | Percorso DB SQLite per checkpoint produzione |
| `enable_spacy_heuristics` | `True` | Abilita estrazione euristica spaCy |
| `heuristic_mapping_confidence_threshold` | variabile | Soglia per mapping euristico in lazy mode |

### Stato iniziale (`BuilderState`)

Lo stato e un `TypedDict` con campi principali:
- `chunks`, `triplets`, `entities`, `tables`, `enriched_tables`
- `pending_tables`, `completed_tables`, `current_table`
- `mapping_proposal`, `best_proposal`, `current_cypher`
- `reflection_prompt`, `reflection_attempts`
- `cypher_failed`, `hitl_flag`, `skip_hitl`
- `trace_enabled`, `builder_trace`, `trace_output_dir`

## 8. Testing e Verifica

### Unit tests
- Test dei nodi individuali con mock LLM (fixture `mock_llm`)
- Test routing `_route_after_validate` con combinazioni di flag
- Test `_route_after_build` con/senza pending_tables
- Test `build_builder_graph()` ritorna un grafo compilato

### Integration tests (richiedono Neo4j)
- Test end-to-end `run_builder()` con documenti di test
- Verifica che nodi BusinessConcept e PhysicalTable siano creati
- Verifica archi MAPPED_TO, REFERENCES, MENTIONS
- Verifica idempotenza: secondo run non duplica nodi

### Comandi
```bash
pytest tests/unit/ -v -k "builder"
pytest tests/integration/ -v -k "builder"
```

## 9. Note di Manutenzione ed Estensione

### Aggiunta di un nuovo nodo
1. Implementare la funzione nodo con signature `(state: BuilderState) -> dict`
2. Aggiungerla con `graph.add_node("nome", funzione)` in `build_builder_graph()`
3. Collegare con `graph.add_edge()` o `graph.add_conditional_edges()`
4. Aggiornare `BuilderState` in `src/models/state.py` se servono nuovi campi

### Modifica del flusso di validazione
Il nodo `_node_validate_mapping` implementa il pattern Actor-Critic con best-proposal tracking. Per modificare il comportamento:
- Cambiare la soglia `confidence_threshold` per HITL
- Disabilitare il critic via `enable_critic_validation=False`
- Modificare `max_reflection_attempts` per piu/meno tentativi

### Produzione vs sviluppo
- `production=True`: usa `SqliteSaver`, `interrupt_before=["hitl"]`
- `production=False`: usa `MemorySaver`, no interrupt (auto-accept HITL)

### Debug tracing
Il parametro `trace_enabled=True` in `run_builder()` abilita il salvataggio di trace dettagliate in JSONL, utili per l'analisi degli esperimenti di ablation.

## 10. Riferimenti

1. LangGraph Documentation -- https://langchain-ai.github.io/langgraph/
2. LangChain Documentation -- https://python.langchain.com/
3. Epic EP-11, User Story US-11-01: "Builder Graph Orchestration" in `docs/draft/REQUIREMENTS.md`
4. Prompt templates: `CYPHER_SYSTEM`, `CYPHER_USER`, `CYPHER_FIX_USER` in `src/prompts/templates.py`
5. Few-shot examples: `src/prompts/few_shot.py` -- `load_cypher_examples()`
6. Schema definitions: `src/models/schemas.py` -- `MappingProposal`, `Entity`, `EnrichedTableSchema`
7. State definition: `src/models/state.py` -- `BuilderState`
