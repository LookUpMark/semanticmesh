# Parte 2 — Modelli Dati e Prompt Templates

Dopo aver stabilito l'infrastruttura nella Parte 1, era il momento di definire i contratti che il sistema avrebbe dovuto rispettare. La Parte 2 si concentra su due aspetti complementari: i modelli dati che definiscono come le informazioni fluiscono attraverso il sistema, e i prompt templates che istruiscono i LLM su cosa fare con quelle informazioni.

## TASK-05: Schemi Pydantic per tutto il Pipeline

La decisione di raccogliere tutti i modelli Pydantic in un unico file, `src/models/schemas.py`, nasce da una considerazione pratica: avere import unambigui. Invece di dover ricordare se una certa classe è definita in `models/extraction.py` o `models/mapping.py`, tutto è in un posto. Questo approccio, che inizialmente poteva sembrare eccessivamente centralizzato, si è rivelato prezioso man mano che il sistema cresceva in complessità.

Il file è organizzato per sezioni che seguono il flusso logico del sistema. Prima ci sono i modelli per l'ingestion — `Document` per una pagina PDF estratta, `Chunk` per un segmento di testo. Poi quelli per l'estrazione — `Triplet` per una tripletta soggetto-predicato-oggetto con la sua provenance testuale. Seguono i modelli per la risoluzione delle entità — `EntityCluster` per un gruppo di varianti raggruppate dal blocking, `CanonicalEntityDecision` per la decisione del LLM judge.

Una particolarità importante è `EnrichedTableSchema`, che estende `TableSchema` invece di sostituirlo. Questo design choice, permesso da Pydantic v2, significa che ovunque nel codice ci si aspetti un `TableSchema`, si può passare un `EnrichedTableSchema` senza violare i type checker. Questo ha semplificato notevolmente il codice, evitando di dover duplicare funzioni che lavorano con entrambi i tipi.

Ciascun modello è accompagnato da validatori che assicurano l'integrità dei dati. Per esempio, il campo `confidence` di `Triplet` è definito come `Field(ge=0.0, le=1.0)`, garantendo che i valori siano sempre nel range valido. Questi controlli a runtime, combinati con il type checking statico di mypy, hanno prevenuto numerosi bug durante lo sviluppo.

## TASK-06: Stati LangGraph per Grafi Complessi

LangGraph richiede che lo stato del grafo sia definito come `TypedDict`, non come Pydantic models. È una limitazione del framework che ha richiesto un file separato, `src/models/state.py`, per definire `BuilderState` e `QueryState`.

Il `BuilderState` descrive lo stato del grafo di costruzione della Knowledge Graph. Contiene campi obbligatori come `documents` e `tables` che rappresentano l'input del sistema, e campi opzionale usando `NotRequired` per tutti i dati intermedi — chunks, triplets, entities, mappings, cypher statements. Questa distinzione tra input obbligatorio e dati opzionale generati durante l'esecuzione permette al grafo di validare l'input iniziale mentre rimanendo flessibile sui dettagli interni.

Il `QueryState` segue lo stesso pattern per il grafo di interrogazione Agentic RAG. L'input è la `user_query`, e tutti gli altri campi — chunks recuperati, risposta generata, decisione del grader — sono opzionali e popolati durante l'esecuzione.

Le sette unit test per questi stati verificano che i TypedDict funzionino come previsto, che i campi opzionali siano effettivamente opzionali, e che i valori default siano appropriati.

## TASK-07: Catalogo Centralizzato dei Prompt

Uno dei rischi più grandi nei sistemi che usano LLM è avere prompt sparsi per il codebase, difficili da trovare e ancora più difficili da versionare. Per questo ho creato un catalogo centralizzato in `src/prompts/templates.py` che contiene tutti e undici i prompt templates del sistema.

Ogni prompt è definito come una costante Python con un nome mnemonico: `EXTRACTION_SYSTEM` per l'estrazione delle triplette, `MAPPING_SYSTEM` per il mapping semantico, `ENRICHMENT_SYSTEM` per l'espansione degli acronimi, e così via. I prompt user contengono placeholder in formato `.format()` che vengono popolati a runtime con i dati specifici del contesto.

La decisione di usare stringhe Python invece di file esterni è stata deliberata. Le stringhe sono tracciate in git, permettendo di vedere come i prompt cambiano nel tempo. Sono anche facilmente accessibili nell'IDE, permettendo di modificare un prompt senza dover navigare tra file. Infine, il type checker può verificare che i placeholder esistano, riducendo la possibilità di errori a runtime.

I sei unit test per questo modulo verificano che tutti i prompt esistano, che i placeholder siano validi, e che il formatting funzioni correttamente.

## TASK-08: Esempi Few-Shot Dinamici

Gli esempi few-shot sono uno degli strumenti più potenti per migliorare la qualità degli output LLM. Invece di codificare gli esempi direttamente nei prompt, ho implementato un sistema di caricamento dinamico in `src/prompts/few_shot.py`.

La funzione `load_cypher_examples()` legge esempi Cypher da un file JSON, permettendo di aggiungere, rimuovere o modificare esempi senza toccare il codice. La funzione `format_cypher_examples()` poi formatta questi esempi per l'iniezione nel prompt, permettendo di selezionare solo gli esempi più rilevanti per il contesto corrente.

Questo approccio dinamico ha un vantaggio importante: permette di adattare gli esempi al contesto specifico. Per esempio, quando si genera Cypher per una tabella con molte colonne, il sistema può preferire esempi di tabelle complesse. Per una tabella semplice, può usare esempi più semplici. Questa adattabilità migliora la qualità dell'output senza dover codificare logica complessa nel prompt stesso.

Le nove unit test per questo modulo verificano che il caricamento funzioni anche con il percorso di default, che il formatting produca output corretto, e che il sistema gestisca gracefulmente i file mancanti.

## Il Valore di Contratti Chiari

Insieme, questi quattro task hanno stabilito contratti chiari per tutto il resto del sistema. I modelli Pydantic definiscono che forma hanno i dati. Gli stati LangGraph definiscono come i dati fluiscono attraverso i grafi. I prompt templates definiscono come i LLM dovrebbero processare quei dati. E il sistema few-shot fornisce esempi concreti che guidano i LLM verso output di qualità.

Questa fondazione di contratti chiari ha semplificato notevolmente lo sviluppo delle parti successive. Quando implementavo l'estrazione delle triplette, sapevo esattamente che forma doveva avere l'output — un `TripletExtractionResponse` con una lista di oggetti `Triplet`. Quando implementavo il mapping, sapevo che il modello LLM avrebbe prodotto un `MappingProposal` con confidence score e reasoning.

Non dovevo inventare strutture dati al volo o preoccuparmi di incompatibilità tra componenti. Tutto era definito upfront, e il mio compito era semplicemente implementare la logica che trasformava input definiti in output definiti. Questa chiarezza ha ridotto i bug, semplificato il testing, e reso il codebase più manutenibile.

---

### Riferimenti

Per i dettagli implementativi di ciascun task, consulta le guide dettagliate:
- [`schemas.py`](../implementation/part-2-models-prompts/05-schemas.md) — Tutti i modelli Pydantic
- [`state.py`](../implementation/part-2-models-prompts/06-state.md) — Stati LangGraph
- [`templates.py`](../implementation/part-2-models-prompts/07-templates.md) — Prompt templates
- [`few_shot.py`](../implementation/part-2-models-prompts/08-few-shot.md) — Esempi few-shot
