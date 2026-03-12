# Parte 7 — Retrieval Ibrido

Con il Knowledge Graph costruito e popolato su Neo4j, il sistema deve poter recuperare informazioni rilevanti in risposta alle query degli utenti. La Parte 7 implementa un sistema di retrieval ibrido a tre canali che combina dense vector search, BM25 keyword search, e graph traversal, con RRF (Reciprocal Rank Fusion) per combinare i risultati e cross-encoder reranking per precision refinement.

## TASK-23: Embeddings BGE-M3 per Dense Vector Search

La prima decisione architetturale per il retrieval è stata la scelta del modello embedding. Ho selezionato BGE-M3 (BAAI/bge-m3) per diversi motivi. Primo, è un modello multilingue che supporta oltre 100 lingue — cruciale per domini dove la documentazione potrebbe contenere termini in diverse lingue. Secondo, produce vettori 1024-dimensionali che bilanciano expressiveness e efficiency — abbastanza grandi da catturare sfumature semantiche, abbastanza piccoli da essere efficienti da calcolare e confrontare.

Terzo, e forse più importante, BGE-M3 può generare tre tipi di embeddings: dense, sparse, e multi-vector. Anche se in questo sistema uso solo gli embeddings dense, la flessibilità del modello significa che in futuro potrei sperimentare con embeddings sparse senza dover cambiare modello.

Il wrapper `BGE_M3_Embedder` in `src/retrieval/embeddings.py` incapsula la complessità di lavorare con sentence-transformers. Gestisce il caricamento del modello, la normalizzazione dei vettori (importante per cosine similarity), e il batch encoding per efficienza. La normalizzazione a unit vectors semplifica il calcolo di similarità — con vettori normalizzati, la cosine similarity diventa semplicemente il dot product.

## TASK-24: Hybrid Retriever con RRF Fusion

La seconda decisione architetturale è stata di usare tre canali di retrieval invece che affidarsi a un singolo metodo. Ogni canale ha punti di forza e debolezza diversi, e combinarli produce risultati più robusti.

Il canale dense vector usa gli embeddings BGE-M3 per trovare documenti semanticamente simili alla query. Eccelle per trovare concetti correlati anche quando usano termini diversi — "Customer" e "Client" saranno vicini nello spazio embedding. Il canale BM25 keyword search invece eccelle per termini esatti — se l'utente cerca un termine tecnico specifico come "DDL_SOURCE", BM25 lo troverà anche se quel termine è raro nel corpus.

Il terzo canale, graph traversal, è unico. Sfrutta la struttura del Knowledge Graph su Neo4j: partendo dai nodi che matchano la query, traversa le relationships per trovare nodi correlati. Questo permette di recuperare informazioni che non sarebbero trovate da search testuale — per esempio, tutte le tabelle che sono mapped allo stesso concetto, o tutti i concetti che sono related a un concetto dato.

Combinare questi tre canali richiede un metodo che non richieda tuning di weights. Ho scelto Reciprocal Rank Fusion (RRF), un algoritmo semplice ma potente. Per ogni documento nei risultati, calcola `1/(k + rank)` dove `k` è una costante (tipicamente 60) e `rank` è la posizione nel ranking. Poi somma questi punteggi attraverso tutti i canali. Un documento che è primo in un canale ma non appare negli altri avrà punteggio `1/60 ≈ 0.0167`. Un documento che è terzo in due canali avrà punteggio `1/63 + 1/63 ≈ 0.0317`.

Il beauty di RRF è che non richiede weight tuning. I pesi sono impliciti nella formula — ogni canale contribuisce equamente, e l'algoritmo gestisce automaticamente casi dove un documento appare in alcuni canali ma non altri.

## TASK-25: Cross-Encoder Reranking per Precision

L'ultimo passo nel retrieval è il reranking. L'hybrid retriever produce una lista di candidati, ma l'ordine potrebbe non essere ottimale per la query specifica. Il cross-encoder reranker affina questo ordine.

A differenza del bi-encoder (BGE-M3) che produce embeddings per documenti indipendentemente dalla query, il cross-encoder prende coppie query-documento e produce un relevance score per ogni coppia. Questo è più accurato ma anche più lento — ogni query-document pair richiede un forward pass through il modello.

Il compromesso è usare il bi-encoder per retrieval veloce (recupera top-30 candidates), e il cross-encoder per reranking preciso (riordina quei 30 a top-10). Questo two-stage approach bilancia velocità e accuratezza.

Il modello scelto per il reranking è bge-reranker-large, ottimizzato specificamente per questo task. Produce un singolo score per coppia query-documento, e i documenti vengono riordinati secondo questi score. Il `reranker_score` viene aggiunto al `RetrievedChunk` come metadata, permettendo di confrontare gli score pre e post reranking per debugging.

## Retrieval per Agentic RAG

Insieme, questi tre task implementano un sistema di retrieval che è stato progettato specificamente per le esigenze dell'Agentic RAG. L'hybrid approach con RRF fornisce copertura robusta across diversi tipi di query. Il reranking cross-encoder aggiunge precisione per le query più importanti. E tutto è integrato in un `HybridRetriever` che può essere chiamato con una singola funzione `query()`.

Questo sistema di retrieval diventa un componente critico del Query Graph (Parte 8), dove fornisce i context chunks che il generatore userà per produrre risposte. La qualità del retrieval influenz direttamente la qualità delle risposte, quindi ogni miglioramento in questa parte ha effetti a cascata sull'intero sistema.

---

### Riferimenti

Per i dettagli implementativi di ciascun task, consulta le guide dettagliate:
- [`embeddings.py`](../implementation/part-7-retrieval/23-embeddings.md) — BGE-M3 embedder
- [`hybrid_retriever.py`](../implementation/part-7-retrieval/24-hybrid-retriever.md) — Hybrid retriever con RRF
- [`reranker.py`](../implementation/part-7-retrieval/25-reranker.md) — Cross-encoder reranker
