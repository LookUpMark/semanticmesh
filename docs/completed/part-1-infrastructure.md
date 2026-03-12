# Parte 1 — Infrastruttura e Configurazione

Prima di costruire un sistema multi-agente complesso per il Knowledge Graph construction e l'Agentic RAG, era necessario stabilire delle fondamenta solide. La Parte 1 del progetto si occupa proprio di questo: creare l'infrastruttura su cui tutto il resto sarebbe stato costruito. Cinque task compongono questa parte, ognuno dei quali risponde un esigenza critica del sistema.

## TASK-01: Il cuore del progetto — pyproject.toml

Tutto inizia con `pyproject.toml`, il file che definisce l'identità del progetto. Ho scelto di utilizzare il formato PEP 621, lo standard moderno per la configurazione dei pacchetti Python, perché rende il progetto più interoperabile e meno dipendente da tool specifici. All'interno di questo file ho definito non solo le dipendenze principali del progetto — LangChain per orchestrazione, Pydantic per la validazione dei dati, Neo4j per il database grafo, sqlglot per il parsing SQL, sentence-transformers per gli embeddings — ma anche gruppi di dipendenze opzionali per sviluppo, testing e documentazione.

Il file `.env.example` completa questo quadro fornendo un template per tutte le variabili d'ambiente che il sistema necessita. Queste includono le credenziali per Neo4j, le chiavi API per i servizi LLM, i nomi dei modelli da utilizzare per diverse tipologie di task (reasoning, estrazione, generazione), e vari parametri configurativi come le soglie di confidenza e i limiti di retry. Avere un file di esempio permette a chiunque di configurare rapidamente un ambiente di sviluppo senza dover indovinare quali variabili siano necessarie.

## TASK-02: Configurazione centralizzata con Pydantic

Una delle prime decisioni architetturali importanti è stata quella di usare Pydantic per la gestione della configurazione. La classe `Settings` in `src/config/settings.py` funge da punto di accesso centralizzato per tutte le impostazioni del sistema. Pydantic non solo carica le variabili d'ambiente dal file `.env`, ma le valida anche al volo, prevenendo errori di configurazione prima ancora che il sistema parta.

Per esempio, se qualcuno configura erroneamente una soglia di confidenza come `1.5` invece di un valore tra `0.0` e `1.0`, Pydantic rifiuterà immediatamente quel valore con un errore di validazione chiaro. Questo type-safety a runtime è inestimabile in un sistema complesso dove una configurazione errata potrebbe portare a risultati difficili da debuggare. Inoltre, usando mypy in modalità strict, ho potuto garantire che anche il type checking statico catturi errori prima dell'esecuzione.

Le cinque unit test per questo modulo verificano tre aspetti critici: l'override delle variabili d'ambiente funziona correttamente, la validazione dei range previene valori fuori scala, e i valori default sono appropriati per un ambiente di sviluppo locale.

## TASK-03: Logging strutturato per LangGraph

In un sistema basato su grafi come LangGraph, capire cosa succede in ogni nodo è fondamentale per il debugging e il monitoraggio. Per questo ho implementato un sistema di logging strutturato in JSON usando `python-json-logger`. La funzione `log_node_event()` permette di loggare eventi in ogni nodo con metadati consistenti: nome del nodo, tipo di evento (start, end, error), timestamp, e qualsiasi altra informazione rilevante per quel nodo specifico.

Il `NodeTimer`, un context manager, semplifica ancora di più le cose: racchiudendo l'esecuzione di un nodo in un blocco `with`, il tempo di esecuzione viene automaticamente calcolato e aggiunto al log. Questo è particolarmente utile per identificare colli di bottiglia nel pipeline.

Il formato JSON dei log è stato scelto deliberatamente perché permette di parsare e analizzare i logs in modo automatizzato. Un log tipico dopo l'esecuzione di un nodo di estrazione delle triplette potrebbe apparire così:

```json
{
  "node": "extract_triplets",
  "event": "end",
  "timestamp": "2026-03-12T10:30:45",
  "elapsed_ms": 1234,
  "triplets_extracted": 15,
  "model": "claude-3-haiku"
}
```

Questo livello di dettaglio permette di ricostruire esattamente cosa è successo durante un'esecuzione, quanto tempo ha richiesto ogni operazione, e quali LLM sono stati utilizzati.

## TASK-04: Factory pattern per i LLM

Uno dei principi guida dell'architettura è il provider-agnosticism: non volevo che il sistema fosse legato a un particolare fornitore di LLM. Il modulo `llm_factory.py` implementa un pattern Factory che permette di switchare tra diversi provider semplicemente cambiando una variabile d'ambiente.

Il factory fornisce tre tipi di LLM, ognuno ottimizzato per un tipo specifico di task. Per il reasoning complesso — decisioni che richiedono analisi profonda come il giudizio di merge delle entità — uso `get_reasoning_llm()`, che ritorna un modello con temperatura 0.0 per output deterministici. Per l'estrazione di dati strutturati — triplette, mapping, Cypher — uso `get_extraction_llm()`, anch'esso con temperatura 0.0 perché vogliamo output JSON validi e riproducibili. Infine, per la generazione di testo fluente — risposte alle domande, descrizioni — uso `get_generation_llm()` con una temperatura leggermente più alta (0.3) che permette un po' più di creatività mantenendo la factualness.

Questo approccio modulare significa che posso passare da OpenRouter a OpenAI, Anthropic, o un modello locale Ollama semplicemente cambiando `settings.llm_model_reasoning` e ricreando le istanze LLM dal factory. Le sei unit test verificano che il factory ritorni sempre il tipo corretto di LLM con la temperatura appropriata.

## TASK-04b: InstrumentedLLM — Retry, Logging e Token Tracking

Anche con i migliori LLM, le cose possono andare storte. Rate limit, timeout di rete, o errori temporanei del provider sono tutti casi che un sistema di produzione deve gestire graziosamente. La classe `InstrumentedLLM` in `src/config/llm_client.py` è un proxy wrapper che aggiunge tre capacità critiche a qualsiasi modello BaseChatModel di LangChain.

Prima, la logica di retry. Quando il wrapped LLM solleva una `RateLimitError` o `APITimeoutError`, `InstrumentedLLM` ritenta automaticamente la richiesta fino a tre volte (configurabile via `settings.max_llm_retries`). Il backoff è esponenziale con jitter per evitare di sovraccaricare ulteriormente il servizio durante un periodo di stress. Ogni tentativo di retry viene loggato con `log_retry_event()`, permettendo di tracciare quanto spesso i retry si attivano e identificare problemi sistemici.

Secondo, il logging della latenza. Ogni chiamata a `invoke()` o `ainvoke()` viene misurata, e il tempo impiegato viene loggato insieme al nome del modello. Questo permette di costruire un quadro chiaro delle performance del sistema nel tempo e identificare quali nodi richiedono ottimizzazione.

Terzo, il tracking dei token. Anche se non completamente implementato in questa versione, l'infrastruttura per tracciare l'uso dei token è in atto, permettendo in futuro di attribuire i costi LLM a specifiche operazioni del pipeline.

Un aspetto particolarmente elegante di `InstrumentedLLM` è il suo uso di `__getattr__` per delegare qualsiasi attributo non esplicitamente override al modello sottostante. Questo significa che funzionalità come `bind_tools()` o `with_structured_output()` di LangChain continuano a funzionare senza modifiche, rendendo il wrapper veramente trasparente.

Le quattordici unit test per questo modulo verificano che il wrapper soddisfa il protocollo LLMProtocol, che la logica di retry funziona come previsto, che la delega degli attributi funziona correttamente, e che il logging avviene appropriatamente.

## Conclusione della Parte

Alla fine di questi cinque task, l'infrastruttura del sistema era solida e pronta a supportare le componenti più complesse che sarebbero seguite. Il dependency management tramite PEP 621 rende il progetto standard e interoperabile. La configurazione Pydantic garantisce type-safety e validazione. Il logging strutturato permette debug efficace e monitoraggio produttivo. Il factory pattern per i LLM permette flessibilità nella scelta del provider. E l'InstrumentedLLM wrapper aggiunge resilienza e osservabilità.

Questa fondazione ha permesso di costruire il resto del sistema con la confidenza che gli aspetti infrastrutturali erano gestiti in modo robusto e scalabile. Quando ho iniziato a lavorare sulle parti successive — modelli dati, prompts, ingestion, extraction — ho potuto concentrarmi sulla logica di business sapendo che l'infrastruttura sottostante sarebbe stata affidabile.

---

### Riferimenti

Per i dettagli implementativi di ciascun task, consulta le guide dettagliate:
- [`pyproject.toml`](../implementation/part-1-infrastructure/01-pyproject.md) — Configurazione progetto e dipendenze
- [`settings.py`](../implementation/part-1-infrastructure/02-settings.md) — Pydantic settings centralizzati
- [`logging.py`](../implementation/part-1-infrastructure/03-logging.md) — Logging strutturato JSON
- [`llm_factory.py`](../implementation/part-1-infrastructure/04-llm-factory.md) — Factory pattern per LLM
- [`llm_client.py`](../implementation/part-1-infrastructure/04b-llm-client.md) — InstrumentedLLM wrapper
