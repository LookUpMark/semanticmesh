# Parte 8 — Generazione e Query Graph

L'ultimo pezzo del puzzle è generare risposte alle domande degli utenti usando il Knowledge Graph. La Parte 8 implementa l'answer generation con Self-RAG (Self-Reflective Retrieval-Augmented Generation), l'hallucination grading per detectare risposte non supportate, il web search fallback per context irrelevant, e il Query Graph completo che orchestra l'intero workflow Agentic RAG.

## TASK-26: Answer Generation Context-Aware

La funzione `generate_answer()` in `src/generation/answer_generator.py` implementa il cuore del sistema di risposta. Prende una query utente e i chunks recuperati dal sistema di retrieval, e genera una risposta usando un LLM con temperatura 0.3 — abbastanza bassa per factualness, abbastanza alta per fluency.

Il prompt ANSWER_SYSTEM istruisce il LLM a rispondere SOLO dalle informazioni nel context recuperato. Se la risposta non è presente nel context, il LLM deve usare esattamente la frase "I cannot find this information in the knowledge graph." Questo è cruciale per prevenire hallucination — il LLM non deve inventare informazioni che non sono nel grafo.

Il context viene formattato come una lista di chunk, ognuno prefissato con il suo node_type (BusinessConcept o PhysicalTable) e il suo text. Questo aiuta il LLM a capire la provenienza di ogni informazione e a citare le fonti appropriatamente nella risposta.

Se una risposta viene generata ma il grader la trova non supportata (vedi TASK-27), la funzione `regenerate_with_critique()` viene chiamata. Questa funzione inietta la critique nel prompt, istruendo il LLM a evitare specificamente gli errori menzionati e a rimanere strettamente nel context.

## TASK-27: Hallucination Grading con Self-RAG

Una delle sfide più grandi nei sistemi RAG è l'hallucination — il LLM genera risposte che sembrano plausibili ma contengono informazioni non supportate dal context. L'hallucination grader in `src/generation/hallucination_grader.py` implementa il paradigma Self-RAG per detectare questi casi.

Il grader prende la query, la risposta generata, e i context chunks, e produce un `GraderDecision` con tre campi: `grounded` (boolean), `critique` (stringa opzionale), e `action` ("pass", "regenerate", o "web_search").

Il caso più semplice è quando la risposta è fully grounded — tutte le affermazioni sono supportate dal context. In questo caso `grounded=True`, `critique=None`, e `action="pass"`. Il sistema accetta la risposta e la ritorna all'utente.

Più interessante è il caso quando la risposta contiene claims non supportati. Qui `grounded=False`, la `critique` deve specificare esattamente quale entità o affermazione non è supportata, e `action="regenerate"`. La critique deve essere specifica — non basta dire "alcune claims non sono supportate", deve dire "Table TB_ORD is not mentioned in any retrieved context chunk. Reformulate the answer omitting TB_ORD."

Il terzo caso è quando il context recuperato è completamente unrelated alla query. Qui il sistema non dovrebbe rigenerare la risposta — non servirebbe a nulla perché il context è sbagliato. Invece, `action="web_search"` e il sistema attiva il fallback.

## TASK-28: Query Graph con Conditional Routing

Il `QueryGraph` in `src/generation/query_graph.py` è l'orchestratore finale che combina tutti i componenti delle parti precedenti in un workflow Agentic RAG completo. Esegue in sequenza: retrieval, reranking, generation, grading, e poi conditional routing basato sulla decisione del grader.

Il routing è implementato con `add_conditional_edges()` di LangGraph. Dopo il grading, se la risposta è grounded, il grafo termina e ritorna la risposta all'utente. Se la risposta non è grounded ma il context è rilevante, il grafo rigenera la risposta con la critique e poi la ri-grada. Se il context è completamente irrelevant, il grafo attiva il web search fallback e poi genera una nuova risposta basata su quel context.

Questo routing condizionale implementa un loop di miglioramento: il sistema genera una risposta, la valuta, e se non è buona la migliora. Questo continua fino a tre tentativi di regeneration, dopo di cui il sistema accetta l'ultima risposta anche se non perfetta. Questo limite impedisce loop infiniti su query difficili.

## Dai Grafi LangGraph al Sistema Completo

Con il Query Graph completato, il sistema implementa ora due grafi LangGraph che lavorano insieme:

1. **Builder Graph** (Parte 6): Costruisce il Knowledge Graph da documenti PDF e DDL SQL
2. **Query Graph** (Parte 8): Interroga il Knowledge Graph per rispondere a domande utenti

Questa architettura a due grafi separa chiaramente due fasi distinte: la fase di costruzione (offline, batch) e la fase di interrogazione (online, latency-sensitive). Il Builder Graph può essere eseguito periodicamente per aggiornare il grafo con nuovi documenti o modifiche allo schema DB. Il Query Graph risponde alle query degli utenti usando il grafo corrente.

L'intero sistema — dalle 8 parti, dai 28 task completati, dalle centinaia di unit test — rappresenta un'implementazione completa di un sistema Multi-Agent Framework for Semantic Discovery & GraphRAG. Può leggere documenti business PDF, parsare schema DB, estrarre triplette semantiche, risolvere entità, mappare tabelle a concetti, generare Cypher per Neo4j, e rispondere a domande con retrieval augmented generation.

È un sistema complesso, ma ogni componente è stato progettato, implementato, e testato con cura. E la documentazione in `docs/completed/` è qui per aiutare a capire come tutto funziona insieme.

---

### Riferimenti

Per i dettagli implementativi di ciascun task, consulta le guide dettagliate:
- [`answer_generator.py`](../implementation/part-8-generation/26-answer-generator.md) — Answer generation
- [`hallucination_grader.py`](../implementation/part-8-generation/27-hallucination-grader.md) — Self-RAG grading
- [`query_graph.py`](../implementation/part-8-generation/28-query-graph.md) — Query Graph completo
