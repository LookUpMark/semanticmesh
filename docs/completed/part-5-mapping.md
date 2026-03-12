# Parte 5 — Mapping Semantico

Con le entità business estratte dai documenti e le tabelle database parsate dal DDL, il prossimo passo è allinearle. La Parte 5 implementa il mapping semantico tra tabelle fisiche e concetti business usando un approccio RAG-augmented con pattern Map-Reduce, validazione Actor-Critic, e human-in-the-loop per revisione.

## TASK-16: RAG Mapper con Few-Shot Learning

Il cuore del mapping è la funzione `map_table_to_concepts()`, che prende una tabella arricchita e la mappa al concetto business più appropriato. Questo è un problema di retrieval: dato che abbiamo migliaia di entità nel grafo, quali sono quelle rilevanti per questa tabella?

L'approccio usa un retriever ibrido che combina dense vector search, BM25 keyword search, e graph traversal. Per una tabella come `TB_CUST_ORD` (Customer Orders), il retriever trova entità come "Customer", "Order", "Sales", e altre correlate. Poi un LLM seleziona il best match e assegna un confidence score.

Il pattern Map-Reduce qui è implicito. Il "map" è il retrieval che mappa la tabella a un set di candidati. Il "reduce" è il LLM che riduce i candidati a una singola proposta. Questo approccio è più efficiente che chiedere al LLM di considerare tutte le entità — il retriever pre-filtra le candidates, e il LLM si concentra solo su quelle rilevanti.

Gli esempi few-shot giocano un ruolo cruciale. Il sistema ha una bank di esempi di mapping, e seleziona dinamicamente quelli più rilevanti per la tabella corrente. Se la tabella ha tre colonne, preferisce esempi di tabelle semplici. Se ha venti colonne, preferisce esempi di tabelle complesse. Questa adattabilità migliora la qualità del mapping senza dover codificare logica complessa nel prompt.

Il confidence score che il LLM assegna è cruciale per il downstream. Un score di 0.95+ indica near-certain match — il sistema può auto-approvare. Un score di 0.7-0.9 indica probabile match ma con incertezza — richiede revisione umana. Un score sotto 0.7 indica che nessun concetto business corrisponde davvero — la tabella potrebbe essere un sistema table (audit log, cache, etc.) senza controparte business.

## TASK-17: Validazione Actor-Critic

Un mapping proposto dal LLM potrebbe sembrare corretto ma avere problemi sottili. La tabella `TB_PROD` potrebbe essere mappata a "Product", ma un esame più attento rivela che contiene solo product IDs e nient'altro — è probabilmente una tabella di riferimento o cache, non la tabella principale Product. Questo è il tipo di errore che la validazione Actor-Critic cattura.

Il pattern Actor-Critic viene dal reinforcement learning. L'Actor genera una proposta, il Critic la valuta, e se il Critic la respinge, l'Actor riprova con il feedback. Qui applichiamo lo stesso pattern: l'Actor è il mapper LLM che genera il `MappingProposal`, il Critic è un secondo LLM che valuta se la proposta è valida.

Il Critic controlla tre cose: la coerenza (la struttura della tabella corrisponde alla definizione del concetto?), la giustificazione del confidence (il score è appropriato?), e le contraddizioni logiche (ci sono incoerenze nella proposta?). Se trova problemi, ritorna un `CriticDecision` con `approved=False`, un `critique` che descrive il problema, e un `suggested_correction`.

Se la proposta è respinta, il sistema la rigenera con la critique iniettata nel prompt. Questo "reflection loop" continua fino a tre tentativi, dopo di cui il sistema accetta l'ultima proposta anche se non approvata. Questo limite impedisce al sistema di entrare in un loop infinito su casi difficili.

Questa validazione a due fasi — prima Pydantic per validare la struttura, poi Actor-Critic per validare la semantica — aggiunge un layer di sicurezza senza sacrificare flessibilità. Le proposte valide passano rapidamente. Quelle problematiche vengono catturate e corrette.

## TASK-18: Human-in-the-Loop per Confidenza Bassa

Non tutto può essere automatizzato. Ci sono casi in cui nemmeno il validatore Actor-Critic può decidere con certezza, e casi in cui la revisione umana è comunque richiesta per compliance o regulatory reasons. Il sistema HITL in `src/mapping/hitl.py` gestisce questi casi.

La funzione `should_interrupt()` controlla se il confidence score della proposta è sotto la soglia configurata (default 0.90). Se lo è, setta `hitl_required=True` nello stato, che causa LangGraph a interrompere l'esecuzione e attendere input umano. Questo è realizzato tramite il meccanismo `interrupt` di LangGraph, che permette di pausere e riprendere l'esecuzione del grafo.

Quando un umano interviene, può fornire feedback in tre formati: "APPROVE" per accettare la proposta (e boostare il confidence a 1.0), "CHANGE: NewConcept" per specificare il concetto corretto (che diventa il nuovo mapping con confidence massima), o "REJECT: reason" per rifiutare completamente la proposta.

La funzione `resume_from_feedback()` processa questo feedback e aggiorna la proposta di conseguenza. Se l'umano approva, il confidence viene boostato a 1.0 — l'approvazione umana è il segnale più forte di correttezza. Se l'umano specifica un nuovo concetto, quello diventa il mapping con confidence massima. Se l'umano rifiuta, la proposta viene loggata come respinta e il pipeline continua con la tabella unmapped.

Questo approccio bilancia automazione e supervisione umana. La maggior parte dei mapping — quelli con alta confidence — vengono processati automaticamente. Quelli borderline richiedono una rapida revisione umana. E gli errori possono essere corretti prima che vengano scritti nel grafo.

## Il Valore della Validazione Multi-Layer

Questa parte del sistema implementa una filosofia di validazione a layer multipli. Per prima cosa, il mapping iniziale usa un retriever per pre-filtrare candidates — questo riduce lo spazio di ricerca e previene il "lost in the middle" problem dove il LLM perde traccia di opzioni troppo numerose.

Poi, il validatore Actor-Critic aggiunge un secondo opinion. Due LLM sono meglio di uno per catturare errori — l'Actor può focalizzarsi sulla generazione mentre il Critic si specializza nella validazione. E se ancora c'è incertezza, l'umano nel loop fornisce la decisione finale.

Ogni layer aggiunge robustezza senza sacrificare troppo efficienza. Il retriever è veloce e deterministico. Il Critic è più lento ma viene chiamato solo su proposte già ragionevoli. E l'intervento umano è riservato solo per casi incerti — nel tipico utilizzo, meno del 10% dei mapping richiede revisione.

Il risultato è un sistema che può automaticamente mappare la maggior parte delle tabelle, ma che sa quando chiedere aiuto e può incorporare feedback umano per migliorare continuamente.

---

### Riferimenti

Per i dettagli implementativi di ciascun task, consulta le guide dettagliate:
- [`rag_mapper.py`](../implementation/part-5-mapping/16-rag-mapper.md) — RAG-augmented mapping
- [`validator.py`](../implementation/part-5-mapping/17-validator.md) — Validazione Actor-Critic
- [`hitl.py`](../implementation/part-5-mapping/18-hitl.md) — Human-in-the-loop
