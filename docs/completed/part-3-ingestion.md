# Parte 3 — Ingestion dei Dati

Con l'infrastruttura pronta e i contratti dati definiti, era tempo di affrontare uno dei problemi più fondamentali: come far entrare i dati nel sistema. La Parte 3 copre tre task che rispondono a questa domanda: estrazione di testo dai PDF, parsing di DDL SQL in strutture dati, e arricchimento degli identificatori abbreviati tramite LLM.

## TASK-09: PDF Loader e Chunking Intelligente

L'estrazione di testo dai PDF sembrava un problema risolto, ma la libreria `pymupdf` (alias fitz) ha superato le mie aspettative. A differenza di altre librerie che producono testo disordinato con spazi casuali e newline inopportuni, pymupdf mantiene la struttura del documento in modo affidabile. La funzione `load_pdf()` itera attraverso ogni pagina, estrae il testo, e lo converte in un oggetto `Document` con metadata che traccia il file di origine e il numero di pagina.

Il vero punto critico è stato il chunking. Divide un documento in pezzi troppo piccoli e perdi contesto; chunk troppo grandi e il LLM fatica a elaborarli. Ho usato il `RecursiveCharacterTextSplitter` di LangChain con una strategia intelligente: prova prima a dividere su paragrafi doppi, poi su singoli paragrafi, poi su frasi, e infine su parole. Questo approccio gerarchico preserva la coerenza semantica del testo quanto più possibile.

Ciò che rende questo chunking davvero potente è l'uso di `tiktoken` per contare i token invece dei caratteri. Molti sistemi contano i caratteri, ma i LLM hanno limiti in termini di token, non di caratteri. Un chunk di 512 caratteri di inglese compresso potrebbe contenere più token di uno di 512 caratteri di spaziatura. Contando direttamente i token con l'encodings `cl100k_base` di GPT-4, ho potuto garantire che i chunk rientrino sempre nei limiti del modello.

Un dettaglio particolarmente importante è il `chunk_index` che incrementa sequenzialmente attraverso tutti i documenti. Invece di resettare a 0 per ogni nuovo documento, continua a incrementare. Questo significa che se ho tre documenti che producono rispettivamente 5, 3, e 4 chunk, gli indici saranno 0-4, 5-7, e 8-11. Questo tracciamento unificato si è rivelato prezioso per la provenance tracking in tutto il sistema.

Le undici unit test coprono tutti i casi edge: file non trovati, PDF criptati, PDF corrotti, pagine vuote che vengono saltate, documenti corti che non necessitano chunking, documenti lunghi che producono multipli chunk, e la corretta propagazione dei metadata attraverso l'intero processo.

## TASK-10: Parsing DDL con sqlglot

Se i PDF contengono la conoscenza non strutturata del dominio business, i DDL SQL contengono la struttura formale del database relazionale. Il parsing del DDL è un problema notoriamente difficile perché l'SQL è un linguaggio con numerosi dialetti — MySQL, PostgreSQL, TSQL, Oracle hanno sintassi diverse.

Ho scelto `sqlglot` perché supporta tutti questi dialetti e fornisce un AST (Abstract Syntax Tree) navigabile. La funzione `parse_ddl()` accetta una stringa di DDL e ritorna una lista di oggetti `TableSchema`, ognuno dei quali rappresenta una tabella con le sue colonne, tipi di dati, chiavi primarie, chiavi esterne, e riferimenti.

Il detection delle chiavi primarie e esterne richiede logica particolare. La PK può essere definita a livello di colonna con `PRIMARY KEY` inline, oppure come vincolo di tabella con `CONSTRAINT pk_name PRIMARY KEY (col1, col2)`. Lo stesso vale per le FK, che possono essere definite inline con `REFERENCES other_table(col)` oppure come vincolo di tabella. Il parsing deve gestire entrambi i casi.

Un dettaglio che ho aggiunto è la normalizzazione dei tipi di dati. Un tipo `VARCHAR(200)` in MySQL, `VARCHAR2(200)` in Oracle, e `VARCHAR(200)` in PostgreSQL sono tutti concettualmente la stessa cosa — una stringa di lunghezza variabile. Normalizzandoli tutti a `VARCHAR`, semplifico il downstream processing e riduco la dimensionalità del problema.

Le quattordici unit test per questo modulo coprono parsing di singole tabelle, tabelle multiple, detection di PK e FK, normalizzazione dei tipi, dialetti diversi (incluso PostgreSQL con schema qualificato), e tutti i casi edge come stringhe vuote, DDL senza CREATE TABLE, e solo whitespace.

## TASK-11: Schema Enrichment con LLM

Uno dei problemi più insidiosi nel mapping semantico è il "lexical gap" — quando i nomi nel database sono così diversi dai concetti business che nemmeno un sistema sofisticato può riconoscerli. Una tabella chiamata `TB_CST` con colonne come `CUST_ADDR` e `ORD_DT` potrebbe non sembrare avere nulla a che fare con il concetto "Customer" nel glossario business.

La soluzione è stata usare un LLM per "arricchire" lo schema, espandendo gli acronimi e aggiungendo descrizioni in linguaggio naturale. La funzione `enrich_schema()` prende un `TableSchema` e produce un `EnrichedTableSchema` con campi additivi: `enriched_table_name` (es. "Customer Table"), `enriched_columns` (ogni colonna con un nome leggibile come "Customer Address" invece di "CUST_ADDR"), e `table_description` (una breve descrizione dello scopo business della tabella).

Il prompt per questo task è stato curato particolarmente attentamente. Include regole esplicite per espandere acronomi comuni (CUST→Customer, ORD→Order, HDR→Header, DT→Date, ecc.) e istruzioni per non inventare colonne o dati non presenti nel DDL. La descrizione della tabella deve focalizzarsi su *cosa* dati business contiene, non su come è tecnicamente strutturata.

Un aspetto critico di questo task è il "graceful degradation". Il LLM potrebbe fallire per un timeout di rete, potrebbe restituire JSON invalido, o potrebbe restituire JSON valido ma con campi mancanti. In tutti questi casi, il sistema non deve crashare. Invece, ritorna un `EnrichedTableSchema` con i campi enrichment vuoti, permettendo al pipeline di continuare con gli identificatori originali.

La funzione `enrich_all()` estende questo approccio a multiple tabelle. Anche se una tabella fallisce l'enrichment, le altre continuano. Questo isolation dei fault è cruciale in un sistema di produzione dove un singolo errore non dovrebbe bloccare l'intero pipeline.

Le otto unit test verificano non solo il happy path, ma anche tutti i casi di errore: LLM che fallisce, JSON non valido, JSON parziale con campi mancanti, e il caso in cui una di tre tabelle fallisce ma le altre due hanno successo.

## L'Importanza della Robustezza nell'Ingestion

Questi tre task insegnano una lezione importante: l'ingestion è il punto debole di molti sistemi di produzione. Se l'ingestion fallisce, nulla di quello che segue ha valore. Il PDF loader deve gestire PDF criptati e corrotti. Il DDL parser deve gestire dialetti SQL diversi e sintassi non standard. Lo schema enricher deve degradare gracefulamente quando il LLM fallisce.

Questa robustezza ha pagato dividendi man mano che il sistema cresceva. Quando ho iniziato a lavorare sull'estrazione delle triplette e sul mapping, sapevo che i dati in entrata erano puliti, ben formati, e tracciabili. I documenti erano chunk in modo intelligente. Le tabelle DB erano parsate correttamente con tutti i constraint rilevanti. E gli identificatori erano arricchiti con nomi leggibili che riducevano il lexical gap.

Questa fondazione solida ha permesso alle parti successive di concentrarsi sulla logica di business piuttosto che dover gestire casi edge nell'input. Il risultato è un sistema che, pur essendo complesso, è sorprendentemente affidabile e prevedibile.

---

### Riferimenti

Per i dettagli implementativi di ciascun task, consulta le guide dettagliate:
- [`pdf_loader.py`](../implementation/part-3-ingestion/09-pdf-loader.md) — PDF extraction e chunking
- [`ddl_parser.py`](../implementation/part-3-ingestion/10-ddl-parser.md) — SQL DDL parsing
- [`schema_enricher.py`](../implementation/part-3-ingestion/11-schema-enricher.md) — LLM schema enrichment
