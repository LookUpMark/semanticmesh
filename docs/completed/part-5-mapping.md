# Part 5 — Semantic Mapping

With business entities extracted from documents and database tables parsed from DDL, the next step is to align them. Part 5 implements semantic mapping between physical tables and business concepts using a RAG-augmented approach with Map-Reduce pattern, Actor-Critic validation, and human-in-the-loop review.

## TASK-16: RAG Mapper with Few-Shot Learning

The heart of mapping is the `map_table_to_concepts()` function, which takes an enriched table and maps it to the most appropriate business concept. This is a retrieval problem: given thousands of entities in the graph, which ones are relevant for this table?

The approach uses a hybrid retriever combining dense vector search, BM25 keyword search, and graph traversal. For a table like `TB_CUST_ORD` (Customer Orders), the retriever finds entities like "Customer", "Order", "Sales", and other related concepts. Then an LLM selects the best match and assigns a confidence score.

The Map-Reduce pattern here is implicit. The "map" is the retrieval that maps the table to a set of candidates. The "reduce" is the LLM that reduces candidates to a single proposal. This approach is more efficient than asking the LLM to consider all entities — the retriever pre-filters candidates, and the LLM focuses only on relevant ones.

Few-shot examples play a crucial role. The system has a bank of mapping examples and dynamically selects the most relevant ones for the current table. If the table has three columns, it prefers examples of simple tables. If it has twenty columns, it prefers examples of complex tables. This adaptability improves mapping quality without encoding complex logic in the prompt.

The confidence score the LLM assigns is crucial for downstream processing. A score of 0.95+ indicates a near-certain match — the system can auto-approve. A score of 0.7-0.9 indicates a probable match but with uncertainty — requires human review. A score below 0.7 indicates no business concept really corresponds — the table might be a system table (audit log, cache, etc.) without a business counterpart.

## TASK-17: Actor-Critic Validation

An LLM-proposed mapping might look correct but have subtle issues. Table `TB_PROD` might be mapped to "Product", but closer examination reveals it only contains product IDs and nothing else — it's likely a reference or cache table, not the main Product table. This is the type of error Actor-Critic validation catches.

The Actor-Critic pattern comes from reinforcement learning. The Actor generates a proposal, the Critic evaluates it, and if the Critic rejects it, the Actor retries with feedback. Here we apply the same pattern: the Actor is the mapper LLM that generates the `MappingProposal`, the Critic is a second LLM that evaluates whether the proposal is valid.

The Critic checks three things: coherence (does the table structure match the concept definition?), confidence justification (is the score appropriate?), and logical contradictions (are there inconsistencies in the proposal?). If it finds problems, it returns a `CriticDecision` with `approved=False`, a `critique` describing the problem, and a `suggested_correction`.

If the proposal is rejected, the system regenerates it with the critique injected into the prompt. This "reflection loop" continues up to three attempts, after which the system accepts the last proposal even if not approved. This limit prevents the system from entering an infinite loop on difficult cases.

This two-phase validation — Pydantic first for structure, then Actor-Critic for semantics — adds a layer of security without sacrificing flexibility. Valid proposals pass quickly. Problematic ones are caught and corrected.

## TASK-18: Human-in-the-Loop for Low Confidence

Not everything can be automated. There are cases where even the Actor-Critic validator cannot decide with certainty, and cases where human review is required for compliance or regulatory reasons. The HITL system in `src/mapping/hitl.py` manages these cases.

The `should_interrupt()` function checks if the proposal's confidence score is below the configured threshold (default 0.90). If so, it sets `hitl_required=True` in the state, causing LangGraph to interrupt execution and wait for human input. This is implemented via LangGraph's `interrupt` mechanism, which allows pausing and resuming graph execution.

When a human intervenes, they can provide feedback in three formats: "APPROVE" to accept the proposal (and boost confidence to 1.0), "CHANGE: NewConcept" to specify the correct concept (which becomes the new mapping with maximum confidence), or "REJECT: reason" to completely reject the proposal.

The `resume_from_feedback()` function processes this feedback and updates the proposal accordingly. If the human approves, confidence is boosted to 1.0 — human approval is the strongest signal of correctness. If the human specifies a new concept, it becomes the mapping with maximum confidence. If the human rejects, the proposal is logged as rejected and the pipeline continues with the table unmapped.

This approach balances automation and human supervision. Most mappings — those with high confidence — are processed automatically. Borderline ones require quick human review. And errors can be corrected before being written to the graph.

## The Value of Multi-Layer Validation

This part of the system implements a multi-layer validation philosophy. First, the initial mapping uses a retriever to pre-filter candidates — this reduces search space and prevents the "lost in the middle" problem where the LLM loses track of too many options.

Then, the Actor-Critic validator adds a second opinion. Two LLMs are better than one at catching errors — the Actor can focus on generation while the Critic specializes in validation. And if uncertainty remains, the human in the loop provides the final decision.

Each layer adds robustness without sacrificing too much efficiency. The retriever is fast and deterministic. The Critic is slower but is only called on already reasonable proposals. And human intervention is reserved only for uncertain cases — in typical use, less than 10% of mappings require review.

The result is a system that can automatically map most tables, but knows when to ask for help and can incorporate human feedback for continuous improvement.

---

### References

For implementation details of each task, consult the detailed guides:
- [`rag_mapper.py`](../implementation/part-5-mapping/16-rag-mapper.md) — RAG-augmented mapping
- [`validator.py`](../implementation/part-5-mapping/17-validator.md) — Actor-Critic validation
- [`hitl.py`](../implementation/part-5-mapping/18-hitl.md) — Human-in-the-loop
