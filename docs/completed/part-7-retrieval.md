# Parte 7 — Retrieval Ibrido

Con il Knowledge Graph costruito e popolato su Neo4j, il sistema deve poter recuperare informazioni rilevanti in risposta alle query degli utenti. La Parte 7 implementa un sistema di retrieval ibrido a tre canali che combina dense vector search, BM25 keyword search, e graph traversal, con deduplicazione per mantenere il chunk con score massimo per ogni nodo, e cross-encoder reranking per precision refinement.

## TASK-23: Embeddings BGE-M3 per Dense Vector Search

La prima decisione architetturale per il retrieval è stata la scelta del modello embedding. Ho selezionato BGE-M3 (BAAI/bge-m3) per diversi motivi. Primo, è un modello multilingue che supporta oltre 100 lingue — cruciale per domini dove la documentazione potrebbe contenere termini in diverse lingue. Secondo, produce vettori 1024-dimensionali che bilanciano expressiveness e efficiency — abbastanza grandi da catturare sfumature semantiche, abbastanza piccoli da essere efficienti da calcolare e confrontare.

Terzo, e forse più importante, BGE-M3 può generare tre tipi di embeddings: dense, sparse, e multi-vector. Anche se in questo sistema uso solo gli embeddings dense, la flessibilità del modello significa che in futuro potrei sperimentare con embeddings sparse senza dover cambiare modello.

Il modulo `src/retrieval/embeddings.py` espone tre funzioni pubbliche. `get_embeddings()` è un singleton `@lru_cache` che carica `FlagModel` una volta sola per processo, usando `use_fp16=True` per dimezzare l'utilizzo di VRAM. `embed_texts(texts, model=None)` codifica una lista di stringhe in vettori 1024-dimensionali via `model.encode(batch_size=32)`; se `model` è `None` chiama `get_embeddings()`. `embed_text(text, model=None)` è un wrapper di convenienza per stringa singola. L'import di `FlagEmbedding` è deferred dentro `get_embeddings()` così da non rompere l'importazione del modulo in ambienti CI senza il pacchetto installato.

## TASK-24: Hybrid Retriever con Merge per Score Massimo

La seconda decisione architetturale è stata di usare tre canali di retrieval invece che affidarsi a un singolo metodo. Ogni canale ha punti di forza e debolezza diversi, e combinarli produce risultati più robusti.

Il canale dense vector usa gli embeddings BGE-M3 per trovare documenti semanticamente simili alla query. Eccelle per trovare concetti correlati anche quando usano termini diversi — "Customer" e "Client" saranno vicini nello spazio embedding. Il canale BM25 keyword search invece eccelle per termini esatti — se l'utente cerca un termine tecnico specifico come "DDL_SOURCE", BM25 lo troverà anche se quel termine è raro nel corpus.

Il terzo canale, graph traversal, è unico. Sfrutta la struttura del Knowledge Graph su Neo4j: partendo dai nodi che matchano la query, traversa le relationships per trovare nodi correlati. Questo permette di recuperare informazioni che non sarebbero trovate da search testuale — per esempio, tutte le tabelle che sono mapped allo stesso concetto, o tutti i concetti che sono related a un concetto dato.

Il modulo `src/retrieval/hybrid_retriever.py` espone funzioni standalone: `build_node_index(client)` scarica tutti i nodi `BusinessConcept` e `PhysicalTable` da Neo4j; `vector_search(query, client, top_k, model)` esegue la ricerca vettoriale; `bm25_search(query, all_nodes, top_k)` esegue la ricerca keyword con `BM25Okapi` (import deferred da `rank_bm25`); `graph_traversal(seed_names, client, depth)` espande i nodi seed tramite Cypher. `merge_results(vector, bm25, graph)` deduplicates per `node_id` mantenendo lo score massimo tra i canali, restituendo la lista ordinata per score decrescente.

## TASK-25: Cross-Encoder Reranking per Precision

L'ultimo passo nel retrieval è il reranking. L'hybrid retriever produce una lista di candidati, ma l'ordine potrebbe non essere ottimale per la query specifica. Il cross-encoder reranker affina questo ordine.

A differenza del bi-encoder (BGE-M3) che produce embeddings per documenti indipendentemente dalla query, il cross-encoder prende coppie query-documento e produce un relevance score per ogni coppia. Questo è più accurato ma anche più lento — ogni query-document pair richiede un forward pass through il modello.

Il compromesso è usare il bi-encoder per retrieval veloce (recupera top-N candidates), e il cross-encoder per reranking preciso (riordina quei candidati a top-K). Questo two-stage approach bilancia velocità e accuratezza.

Il modulo `src/retrieval/reranker.py` espone `get_reranker()` (singleton `@lru_cache` che carica `FlagReranker` da `settings.reranker_model`) e `rerank(query, chunks, reranker=None, top_k=None)`. La funzione costruisce le coppie `(query, chunk.text)`, chiama `reranker.compute_score(pairs, normalize=True)`, aggiorna il campo `.score` di ogni `RetrievedChunk` con lo score cross-encoder, ne conserva il valore come `metadata["reranker_score"]` per debugging, e restituisce i top-K ordinati per score decrescente. In caso di eccezione (es. OOM), la funzione degrada gracefully restituendo i chunks nell'ordine originale senza sollevare errori.

## Retrieval per Agentic RAG

Insieme, questi tre moduli implementano un sistema di retrieval progettato specificamente per le esigenze dell'Agentic RAG. Il three-channel approach con deduplicazione per score massimo fornisce copertura robusta across diversi tipi di query. Il reranking cross-encoder aggiunge precisione finale prima che i chunks vengano passati al generatore. La qualità del retrieval influenza direttamente la qualità delle risposte, quindi ogni miglioramento in questa parte ha effetti a cascata sull'intero sistema.

---

### Riferimenti

Per i dettagli implementativi di ciascun task, consulta le guide dettagliate:
- [`embeddings.py`](../implementation/part-7-retrieval/23-embeddings.md) — BGE-M3 embedder singleton
- [`hybrid_retriever.py`](../implementation/part-7-retrieval/24-hybrid-retriever.md) — Three-channel retriever con merge per score massimo
- [`reranker.py`](../implementation/part-7-retrieval/25-reranker.md) — Cross-encoder reranker con graceful degradation
