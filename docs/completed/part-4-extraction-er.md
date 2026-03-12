# Parte 4 — Estrazione e Risoluzione Entità

Con i dati che entrano nel sistema tramite l'ingestion, il prossimo passo è estrarre conoscenza strutturata da quei dati e risolvere le ambiguità. La Parte 4 affronta questo sfida attraverso quattro task che implementano l'estrazione di triplette semantiche e la risoluzione delle entità con un approccio a due stadi.

## TASK-12: Estrazione di Triplette con SLM

L'estrazione di triplette — fatti del tipo "Customer ha Order", "Order contiene Product" — è il cuore della knowledge graph construction. L'approccio che ho implementato usa un Small Language Model (SLM) in modalità JSON, dove il modello riceve un chunk di testo e ritorna una lista strutturata di triplette.

Il punto chiave qui è la temperatura zero. Quando chiedi a un LLM di estrarre triplette, vuoi che sia deterministico. Le stesse triplette dovrebbero essere estratte dallo stesso testo ogni volta. Con temperatura 0.0, il modello diventa essenzialmente una funzione deterministica che mappa input a output, permettendo riproducibilità e testability.

Ciascuna tripla contiene cinque campi: subject, predicate, object, provenance_text, e confidence. Il `provenance_text` è particolarmente importante — è la frase esatta dal documento che supporta la tripla, copiata verbatim. Questo provenance tracking permette di tracciare ogni fatto alla sua fonte, cruciale per la validazione e il debugging futuro. Il campo `confidence`, tra 0.0 e 1.0, permette di filtrare triplette di bassa qualità.

Il sistema deve gestire anche il caso in cui il LLM ritorna una lista invece di un oggetto JSON. Alcuni modelli, quando istruiti a ritornare JSON, ritornano direttamente una lista di triplette. Il codice normalizza questi casi avvolgendo la lista in un oggetto con chiave "triplets".

## TASK-13: Blocking K-NN per Raggruppamento Efficient

Una volta estratte le triplette, ci ritroviamo con centinaia o migliaia di menzioni di entità. Lo stesso concetto potrebbe apparire come "Customer", "customer", "CUST", "Cust.", e altre varianti. Raggruppare queste varianti è un problema computazionalemente costoso — O(n²) se confrontiamo ogni entità con ogni altra.

Il blocking riduce drasticamente questo costo. Invece di confrontare tutte le coppie, usiamo un approccio K-NN (K-Nearest Neighbors) con embeddings BGE-M3. Ogni entità viene convertita in un vettore 1024-dimensionale, e poi troviamo i k-nearest neighbors per ogni entità. Se due entità sono vicine nello spazio embedding (similarità coseno sopra una soglia, default 0.85), le raggruppiamo insieme.

La selezione del candidato canonico per ogni cluster segue una strategia semplice ma efficace: prima scegliamo la forma più frequente tra le varianti, e in caso di parità scegliamo la più lunga. Questo preferisce forme complete rispetto a abbreviazioni — "Customer" verrà scelto su "CUST" se appaiono con la stessa frequenza.

Il valore di avg_similarity per ogni cluster viene usato come segnale di qualità. Un cluster con alta similarità media (0.95+) contiene varianti molto simili e possiamo fidarci che rappresentano lo stesso concetto. Un cluster con bassa similarità (0.75-0.85) contiene varianti più divergenti e richiederà un esame più attento dal LLM judge.

## TASK-14: LLM Judge per Decisioni Semantiche

Il blocking ci dice quali entità *potrebbero* essere la stessa cosa, ma non ci dice se lo sono *effettivamente*. Per questo serve il LLM judge. La funzione `judge_cluster()` prende un `EntityCluster` e un mapa di provenance, e chiede al LLM di decidere se tutte le varianti dovrebbero essere fuse in un'unica entità o mantenute separate.

Ciò che rende questo judge efficace è che basa la sua decisione sul context provenance, non solo sui nomi. Anche se "Customer" e "CUST" sembrano simili come stringhe, se il provenance text mostra che "Customer" appare sempre nel contesto di "Customer Service" mentre "CUST" si riferisce a "CUSTodian", il judge correttamente deciderà di mantenerle separate.

Il ritorno del judge è un `CanonicalEntityDecision` con tre campi: `merge` (boolean), `canonical_name` (il nome finale se merged, o il più specifico se kept separate), e `reasoning` (una frase che spiega la decisione). Il reasoning è loggato ma non usato downstream — serve per debugging e per capire come il judge sta decidendo.

Questa separazione tra blocking (fatto di embeddings, veloce) e judging (fatto di LLM, lento ma più accurato) permette di bilanciare efficienza e accuratezza. Invece di chiamare il LLM per ogni coppia di entità (che sarebbe O(n²) chiamate), chiamiamo il LLM solo per i cluster (che sono tipicamente O(n/10) o anche meno).

## TASK-15: Orchestratore di Entity Resolution

La funzione `resolve_entities()` è l'orchestratore che combina blocking e judging in un pipeline completo. Prima estrae le entità uniche dalle triplette, poi costruisce un mapa di provenance che mappa ogni variante alle frasi in cui appare. Poi esegue il blocking per produrre cluster di candidati, e per ogni cluster chiede al LLM judge di decidere.

Se il judge decide di merged, costruisce un oggetto `Entity` con il nome canonico, una definition creata merging il provenance text delle varianti, una lista di synonyms contenente tutte le varianti, e il provenance text. Se il judge decide di mantenere separate, crea un oggetto `Entity` per ogni variante.

Una caratteristica importante di questo approccio è che è completamente deterministico dato lo stesso input. Gli embeddings sono deterministici. Il blocking K-NN con una soglia fissa è deterministico. E il judge LLM con temperatura 0.0 è deterministico. Questo significa che possiamo eseguire la entity resolution sugli stessi dati multiple volte e ottenere sempre lo stesso risultato — cruciale per riproducibilità scientifica e per test.

## Due Stadi per Accuracy e Efficienza

Questa parte del sistema incarna un principio architetturale importante: usa metodi veloci e grossolani per ridurre lo spazio di ricerca, poi usa metodi lenti ma accurati per le decisioni finali. Il blocking K-NN è veloce — può processare migliaia di entità in secondi — ma non è perfetto. Il LLM judge è lento — richiede una chiamata API per ogni cluster — ma è molto più accurato perché capisce il contesto semantico.

Insieme, questi due stadi producono una resolution che è sia efficiente che accurata. E il fatto che ogni componente è testabile indipendentemente ha permesso di sviluppare e debuggare il sistema in modo modulare. Potevo testare il blocking con mock embeddings, testare il judge con mock LLM, e poi testare l'orchestratore con mock di entrambi.

---

### Riferimenti

Per i dettagli implementativi di ciascun task, consulta le guide dettagliate:
- [`triplet_extractor.py`](../implementation/part-4-extraction-er/12-triplet-extractor.md) — Estrazione triplette SLM
- [`blocking.py`](../implementation/part-4-extraction-er/13-blocking.md) — K-NN blocking con embeddings
- [`llm_judge.py`](../implementation/part-4-extraction-er/14-llm-judge.md) — LLM judge per merge decisioni
- [`entity_resolver.py`](../implementation/part-4-extraction-er/15-entity-resolver.md) — Orchestratore entity resolution
