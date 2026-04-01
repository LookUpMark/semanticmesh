Buonasera,
le scelte fatte fino ad ora mi sembrano tutte ottime. Non ho commenti o motivi per suggerirle delle modifiche. Può procedere su questa strada.



Cordiali saluti,
Paolo Garza



    On 04/03/26 16:10, Marc'Antonio Lopez S336362 wrote:
    Gentile Prof. Garza,

    Le scrivo per aggiornarla sullo stato di avanzamento del mio progetto di tesi magistrale presso DATA REPLY (le ricordo che il titolo proposto è "Generative AI and Foundation Models for Automated Data Engineering and Metadata Orchestration"). Ho cominciato giorni fa la fase di studio e ho ipotizzato l'intera architettura software e la selezione dei framework per il sistema.

    Come concordato, il progetto consiste in un'architettura Multi-Agente per la Data Governance, strutturata in due macro-fasi: Semantic Discovery e GraphRAG. Nella prima fase (Builder Graph), il sistema ingerisce documenti di business non strutturati e schemi fisici di database (DDL) per costruire autonomamente un Knowledge Graph, mappando i concetti logici sulle tabelle fisiche tramite loop di auto-correzione. Nella seconda fase (Query Graph), un motore Advanced GraphRAG interroga l'ontologia generata sfruttando retrieval ibrido e un "firewall cognitivo" (Hallucination Grader) per garantire all'utente finale risposte fattuali e quanto più esenti da allucinazioni.

    Di seguito le principali scelte tecnologiche che ho ipotizzato:

    Orchestrazione Multi-Agente: LangGraph. Ho preferito questa soluzione ad altre alternative per avere un controllo deterministico sui flussi e gestire in modo rigoroso i cicli di "Self-Reflection".

    Graph & Vector Database: Neo4j. Verrà utilizzato come store ibrido (topologia a grafo + similarità vettoriale / BM25) per risolvere il gap lessicale tra business e IT.

    Integrazione LLM: L'architettura è stata disegnata in modo agnostico sfruttando le interfacce standard di LangChain (supportando qualsiasi chat model, che sia OpenAI, Hugging Face, AWS...). Tuttavia, per i test e l'implementazione pratica, utilizzerò la famiglia di modelli Qwen3 tramite l'API gratuita di OpenRouter. Questo mi permette di avere buone performance per i task di estrazione strutturata e generazione codice, aggirando i limiti hardware locali e l'assenza di budget per i costi API. Devo comunque informarmi eventualmente se DATA REPLY, essendo partner associato di AWS, possa mettermi a disposizione magari qualche API per la prototipazione e fase di test.

    Prima di avviare formalmente la fase di implementazione del codice, mi farebbe molto piacere avere un suo parere su questa impostazione. Ritiene che l'architettura e lo stack tecnologico siano sufficientemente solidi per gli obiettivi della tesi o suggerirebbe delle modifiche/integrazioni? Ovviamente l'architettura ipotizzata è ben più complessa di come l'ho descritta qui in mail.

    Qualora lo ritenesse utile, ho preparato una documentazione tecnica dettagliata (inclusi diagrammi di flusso e metriche di valutazione ipotizzate, es. framework RAGAS) che posso inviarle.

    In attesa di un suo riscontro, le porgo cordiali saluti.

    Marc'Antonio Lopez
    s336362