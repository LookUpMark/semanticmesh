# Parte 6 — Grafo Neo4j e Cypher

Con i mapping validati tra tabelle e concetti, il prossimo passo è renderli persistenti in un Knowledge Graph su Neo4j. La Parte 6 implementa l'integrazione Neo4j, la generazione di statement Cypher con few-shot learning, il self-healing per errori di sintassi, e il Builder Graph completo che orchestra tutto.

## TASK-19: Wrapper Neo4j con Helper MERGE

Lavorare direttamente con il driver Neo4j può essere verboso e error-prone. Ogni query deve essere costruita come stringa, i parametri devono essere passati correttamente per prevenire injection, e le sessioni devono essere gestite con cura per evitare connection leaks. Il `Neo4jClient` in `src/graph/neo4j_client.py` incapsula tutta questa complessità.

I tre helper methods — `upsert_concept()`, `upsert_table()`, e `upsert_mapping()` — nascondono la complessità del Cypher MERGE. Il MERGE è cruciale per questo sistema: combina CREATE e MATCH in un'operazione atomica che crea il nodo se non esiste, oppure lo aggiorna se esiste già. Questo rende l'upsert idempotente — possiamo eseguire lo stesso upsert multiple volte senza creare duplicati.

La distinzione tra ON CREATE SET e ON MATCH SET è importante. Alcune proprietà, come il nome del concetto o della tabella, non dovrebbero mai cambiare — vanno in ON CREATE SET. Altre proprietà, come la definition di un concetto o il DDL source di una tabella, dovrebbero essere aggiornate su re-ingestione — vanno in ON MATCH SET. Questa distinzione permette al sistema di essere incrementale: possiamo re-ingestire documenti aggiornati e il grafo verrà aggiornato di conseguenza.

## TASK-20: Generazione Cypher con Few-Shot Examples

Generare Cypher corretto è un problema non banale. Il LLM deve ricordare la sintassi MERGE con i suoi placeholder, deve formattare correttamente le liste di colonne, e deve usare i parametri correttamente. Anche piccoli errori di sintassi — una virgola mancante, un apice non chiuso — possono causare fallimenti.

L'approccio few-shot risolve questo problema fornendo esempi concreti di Cypher corretto. Il sistema ha una bank di esempi, e per ogni tabella seleziona quelli più rilevanti basati sulla similarità (numero di colonne, tipi di dati, ecc.). Questo fornisce al LLM un template da seguire, riducendo drasticamente gli errori.

Un dettaglio importante è che tutti i valori sono passati come parametri — `$concept_name`, `$concept_definition`, etc. — piuttosto che essere hardcoded nella stringa Cypher. Questo previene Cypher injection e migliora la performance perché Neo4j può cachare i query plan.

Il ritorno è un `CypherStatement` che contiene sia il Cypher string che i parametri in un dict separato. Questo permette di eseguire la query con `session.run(cypher, **params)`, che è sia sicuro che efficiente.

## TASK-21: Self-Healing per Errori Cypher

Nonostante i few-shot examples, gli errori accadono. Il LLM potrebbe generare sintassi leggermente sbagliata, potrebbe dimenticare una virgola, o potrebbe usare una keyword in modo non corretto. Invece di fallire completamente, il sistema implementa self-healing.

La funzione `heal_cypher()` esegue un "dry-run" usando EXPLAIN — questo valida la sintassi senza modificare il database. Se trova un errore, inietta l'errore in un prompt di reflection e chiede al LLM di correggere il Cypher. Questo loop continua fino a tre tentativi o finché il Cypher non è valido.

Il prompt di reflection è progettato specificamente per il healing: contiene il Cypher rotto, il messaggio d'errore esatto da Neo4j, e istruzioni per correggere solo l'errore specifico senza ristrutturare inutilmente la query. Questo focus riduce la possibilità che il LLM introduca nuovi errori mentre cerca di correggere quello originale.

In pratica, il self-healing ha un tasso di successo molto alto. La maggior parte degli errori sono problemi minori di sintassi che il LLM corregge al primo tentativo. Gli errori più gravi — per esempio, cercare di usare una feature che non esiste in quella versione di Neo4j — possono richiedere due o tre tentativi ma vengono eventualmente risolti. Solo in rari casi il sistema fallisce dopo tre tentativi, e in quei casi l'errore viene loggato per investigazione manuale.

## TASK-22: Builder Graph Completo

Il `BuilderGraph` in `src/graph/builder_graph.py` è dove tutti i componenti delle parti precedenti vengono assemblati in un pipeline completo. Esegue in sequenza: ingestione PDF, parsing DDL, enrichment schemi, estrazione triplette, risoluzione entità, mapping tabelle-concetti, generazione Cypher, e upsert Neo4j.

Il grafo usa il meccanismo di conditional routing di LangGraph per gestire casi speciali. Dopo il mapping, se il confidence è basso, il grafo interrompe e attende revisione umana. Se il grader approva, continua alla generazione Cypher. Se rifiuta, può rigenerare con feedback.

L'uso di LangGraph per orchestrare questo pipeline ha numerosi vantaggi. Primo, la visualizzazione — possiamo generare un grafo che mostra chiaramente il flusso dei dati e i punti di decisione. Secondo, il debugging — possiamo ispezionare lo stato in ogni nodo per vedere cosa è successo. Terzo, la flessibilità — aggiungere nuovi nodi o modificare il routing è questione di aggiungere o modificare funzioni, non di riscrivere logica complessa.

Il test di integrazione per il Builder Graph esegue l'intero pipeline con dati reali, verificando che il grafo Neo4j risultante contenga i nodi e relationships corretti. Questo test end-to-end è la prova finale che tutte le componenti lavorano insieme correttamente.

## Dall'Ingestion al Grafo

Questa parte rappresenta una transizione importante nel progetto. Nelle parti precedenti, estraevamo e processavamo dati. Qui, finalmente rendiamo quei dati persistenti in un Knowledge Graph strutturato su Neo4j. Questo grafo diventa la fonte di verità per il sistema — è ciò che il Query Graph (Parte 8) interrogherà per rispondere alle domande degli utenti.

Il viaggio da PDF grezzi e DDL SQL a un Knowledge Graph interrogabile è complesso, ma ogni passo è ora ben definito e testato. L'ingestion estrae e pulisce i dati. L'estrazione e la risoluzione entità identificano i concetti business. Il mapping allinea tabelle DB a concetti. Il Cypher generator traduce questi alignements in statement grafo. E il Builder Graph orchestra tutto.

---

### Riferimenti

Per i dettagli implementativi di ciascun task, consulta le guide dettagliate:
- [`neo4j_client.py`](../implementation/part-6-graph/19-neo4j-client.md) — Wrapper Neo4j con helper MERGE
- [`cypher_generator.py`](../implementation/part-6-graph/20-cypher-generator.md) — Generazione Cypher con few-shot
- [`cypher_healer.py`](../implementation/part-6-graph/21-cypher-healer.md) — Self-healing per errori
- [`builder_graph.py`](../implementation/part-6-graph/22-builder-graph.md) — Builder Graph completo
