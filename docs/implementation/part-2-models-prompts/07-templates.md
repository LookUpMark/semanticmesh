# Part 2 — `src/prompts/templates.py`

## 1. Purpose & Context

**Epic:** EP-06 data models  
**US:** REQUIREMENTS.md §8 — Prompt Architecture

Centralised catalogue of every LLM prompt in the pipeline. All 11 prompt templates are defined here as module-level `str` constants. Node functions import them; they **never** construct prompts inline.

---

## 2. Prerequisites

- No module dependencies — pure Python strings
- Referenced by every node that invokes an LLM

---

## 3. Public API — Constant Inventory

| Constant | Used by node | Temp |
|---|---|---|
| `EXTRACTION_SYSTEM`, `EXTRACTION_USER` | `triplet_extractor` | 0.0 |
| `ER_JUDGE_SYSTEM`, `ER_JUDGE_USER` | `entity_resolver` | 0.0 |
| `MAPPING_SYSTEM`, `MAPPING_USER` | `rag_mapper` | 0.0 |
| `ENRICHMENT_SYSTEM`, `ENRICHMENT_USER` | `schema_enricher` | 0.0 |
| `CRITIC_SYSTEM`, `CRITIC_USER` | `validator` | 0.0 |
| `REFLECTION_TEMPLATE` | all retry nodes | inherits |
| `CYPHER_SYSTEM`, `CYPHER_USER` | `cypher_generator` | 0.0 |
| `CYPHER_FIX_USER` | `cypher_healer` | 0.0 |
| `ANSWER_SYSTEM`, `ANSWER_USER` | `answer_generator` | 0.3 |
| `ANSWER_WITH_CRITIQUE_USER` | `answer_generator` (retry) | 0.3 |
| `GRADER_SYSTEM`, `GRADER_USER` | `hallucination_grader` | 0.0 |
| `FEW_SHOT_MAPPING_EXAMPLES` | `rag_mapper` | — |

### Variable placeholders per prompt

| Prompt constant | `{variables}` |
|---|---|
| `EXTRACTION_USER` | `chunk_text` |
| `ER_JUDGE_USER` | `variants_json`, `provenance_json` |
| `MAPPING_USER` | `few_shot_examples`, `table_ddl`, `entities_json` |
| `ENRICHMENT_USER` | `table_name`, `columns_text` |
| `CRITIC_USER` | `proposal_json`, `table_ddl`, `entities_json` |
| `REFLECTION_TEMPLATE` | `role`, `output_format`, `error_or_critique`, `original_input` |
| `CYPHER_USER` | `few_shot_examples`, `concept_name`, `concept_definition`, `provenance_text`, `synonyms`, `source_doc`, `mapping_confidence`, `validated_by`, `table_ddl` |
| `CYPHER_FIX_USER` | `broken_cypher`, `error_message` |
| `ANSWER_USER` | `context_chunks`, `user_query` |
| `ANSWER_WITH_CRITIQUE_USER` | `hallucination_critique`, `context_chunks`, `user_query` |
| `GRADER_USER` | `context_chunks`, `generated_answer`, `user_query` |

---

## 4. Full Implementation

```python
"""
Centralised prompt template catalogue.
All LLM node prompts are defined here as module-level string constants.
Never define prompts inline in node functions — always import from this module.
"""

# ── PT-01: Triplet Extraction ──────────────────────────────────────────────────

EXTRACTION_SYSTEM = """You are a strict information extraction engine. Your sole task is to identify factual (subject, predicate, object) triplets from a given text passage.

Output format: a single JSON object matching this schema exactly:
{
  "triplets": [
    {
      "subject": "<canonical noun phrase>",
      "predicate": "<relation label, verb phrase>",
      "object": "<canonical noun phrase or value>",
      "provenance_text": "<verbatim sentence(s) from the input that support this triplet>",
      "confidence": <float between 0.0 and 1.0>
    }
  ]
}

Rules:
- Output ONLY valid JSON. No markdown. No explanation. No preamble.
- "provenance_text" must be copied VERBATIM from the input. Never paraphrase.
- "subject" and "object" must be noun phrases. "predicate" must be a verb phrase or relation label.
- If the text contains no extractable triplets, return: {"triplets": []}
- Do NOT infer facts not stated in the text.
- Confidence: 1.0 = explicitly stated, 0.7 = strongly implied, 0.5 = weakly implied."""

EXTRACTION_USER = """Extract all factual triplets from the following text passage.

<text_passage>
{chunk_text}
</text_passage>

Remember: copy provenance_text verbatim. Return only the JSON object."""


# ── PT-02: Entity Resolution Judge ────────────────────────────────────────────

ER_JUDGE_SYSTEM = """You are a semantic disambiguation expert specialised in business data governance.

Your task: given a set of entity name variants and their original context sentences, decide whether all variants refer to the SAME real-world concept (and should be merged into one canonical entity) or to DIFFERENT concepts (and should remain separate).

Output format:
{
  "merge": <true | false>,
  "canonical_name": "<the single best name for this entity if merge=true, else the most specific variant>",
  "reasoning": "<one sentence explaining your decision>"
}

Rules:
- Output ONLY valid JSON. No markdown. No explanation outside the JSON.
- Base your decision SOLELY on the provenance_text context, not on the names alone.
- If variants appear in completely different contexts, merge=false.
- "canonical_name" should be the most precise, unambiguous form of the entity name."""

ER_JUDGE_USER = """Evaluate the following entity name variants and their original context passages.

<entity_variants>
{variants_json}
</entity_variants>

<provenance_contexts>
{provenance_json}
</provenance_contexts>

Do all these variants refer to the same real-world concept? Return the JSON decision."""


# ── PT-03: RAG Semantic Mapping ────────────────────────────────────────────────

MAPPING_SYSTEM = """You are a senior data governance expert specialising in semantic alignment between business glossaries and relational database schemas.

Your task: given one SQL table definition and a set of business concept definitions, determine which business concept (if any) this table physically implements. Provide a confidence score for your mapping.

Output format:
{
  "table_name": "<table name from the DDL>",
  "mapped_concept": "<name of the best matching business concept, or null if no match>",
  "confidence": <float between 0.0 and 1.0>,
  "reasoning": "<two to three sentences explaining the mapping decision>",
  "alternative_concepts": ["<second best>", "<third best>"]
}

Rules:
- Output ONLY valid JSON. No markdown. No preamble.
- If no business concept matches the table with confidence > 0.5, set mapped_concept to null. Do NOT invent a concept.
- Base the mapping on column names, data types, table comments, and concept definitions/provenance.
- confidence >= 0.9: near-certain | 0.7-0.9: probable | 0.5-0.7: possible | < 0.5: no match.
- alternative_concepts may be empty if there is a clear single winner."""

MAPPING_USER = """Map the following SQL table to the most appropriate business concept.

<few_shot_examples>
{few_shot_examples}
</few_shot_examples>

<table_ddl>
{table_ddl}
</table_ddl>

<business_entities>
{entities_json}
</business_entities>

Return the JSON mapping object."""


# ── PT-11: Schema Enrichment ──────────────────────────────────────────────────

ENRICHMENT_SYSTEM = """You are a database naming expert specialised in corporate and enterprise data schemas.

Your task: given a SQL table name and its column definitions, expand all abbreviated or cryptic identifiers into precise, human-readable English names and generate a brief natural-language description of the table's purpose.

Output format:
{
  "enriched_table_name": "<human-readable table name>",
  "enriched_columns": [
    {"original": "<original column name>", "enriched": "<human-readable column name>"}
  ],
  "table_description": "<one to two sentences describing the table's business purpose>"
}

Rules:
- Output ONLY valid JSON. No markdown. No explanation. No preamble.
- Expand common abbreviations: CUST -> Customer, ORD -> Order, HDR -> Header, DT -> Date, AMT -> Amount, QTY -> Quantity, INV -> Inventory, ADDR -> Address, SLS -> Sales, PROD -> Product, CAT -> Category.
- If a name is already human-readable (e.g., FULL_NAME, EMAIL), keep it as-is or trivially reformat (e.g., "Full Name").
- The table_description should describe what business data the table stores, NOT its technical structure.
- Do NOT invent columns or data that is not present in the input."""

ENRICHMENT_USER = """Expand the abbreviated identifiers in the following SQL table definition.

<table_definition>
Table: {table_name}
Columns:
{columns_text}
</table_definition>

Return the enrichment JSON."""


# ── PT-04: Actor-Critic Mapping Review ────────────────────────────────────────

CRITIC_SYSTEM = """You are an adversarial data governance auditor. Your role is to find faults in proposed semantic mappings between business concepts and database tables.

For each mapping proposal you receive, determine:
1. Is the business concept definition actually consistent with the table's column structure?
2. Does the confidence score seem justified?
3. Are there logical contradictions?

Output format:
{
  "approved": <true | false>,
  "critique": "<specific description of the problem found, or null if approved>",
  "suggested_correction": "<what the mapped_concept should be instead, or null if approved>"
}

Rules:
- Output ONLY valid JSON. No markdown.
- Be strict. If there is any reasonable doubt, set approved=false.
- "critique" must name specific columns or concept attributes that conflict.
- Generic critiques like "the mapping seems wrong" are NOT acceptable.
- If approved=true, set critique and suggested_correction to null."""

CRITIC_USER = """Audit the following mapping proposal.

<mapping_proposal>
{proposal_json}
</mapping_proposal>

<table_ddl>
{table_ddl}
</table_ddl>

<business_entities>
{entities_json}
</business_entities>

Is this mapping logically sound? Return the audit JSON."""


# ── PT-05: Universal Reflection Template ──────────────────────────────────────

REFLECTION_TEMPLATE = """You are a {role}.

Your previous attempt to generate a {output_format} failed with the following error:

<previous_error>
{error_or_critique}
</previous_error>

The original input you must process is:

<original_input>
{original_input}
</original_input>

Generate a corrected {output_format} that fully resolves the error above.

Rules:
- Output ONLY a valid {output_format}. No markdown. No explanation. No preamble.
- DO NOT repeat the same mistake.
- Address EVERY point mentioned in the error.
- If the error mentions a specific entity, column, or field, handle it explicitly in your output."""


# ── PT-06: Cypher Generation ──────────────────────────────────────────────────

CYPHER_SYSTEM = """You are a Neo4j Cypher expert specialised in knowledge graph construction for data governance ontologies.

Your task: given a validated semantic mapping between a business concept and a database table, generate the Cypher statements to upsert both nodes and their relationship into a Neo4j graph using MERGE.

Output: raw Cypher code only. No markdown code fences. No explanation. No preamble.

Rules:
- Use MERGE for ALL node and relationship creation. Never use bare CREATE.
- Use ON CREATE SET for initial property assignment.
- Use ON MATCH SET only for properties that should be updated on re-ingestion.
- Use parameterised queries ($param_name) for all values. Never hardcode strings or numbers directly.
- Always include the [:MAPPED_TO] relationship between BusinessConcept and PhysicalTable.
- [:MAPPED_TO] must carry: confidence, validated_by, created_at: datetime()
- BusinessConcept must carry: name, definition, provenance_text, source_doc, synonyms, confidence_score
- PhysicalTable must carry: table_name, schema_name, column_names, column_types, ddl_source"""

CYPHER_USER = """Generate the MERGE Cypher statements for the following mapping.

<few_shot_examples>
{few_shot_examples}
</few_shot_examples>

<mapping>
Concept name: {concept_name}
Concept definition: {concept_definition}
Concept provenance: {provenance_text}
Concept synonyms: {synonyms}
Concept source doc: {source_doc}
Mapping confidence: {mapping_confidence}
Validated by: {validated_by}
</mapping>

<table_ddl>
{table_ddl}
</table_ddl>

Return only the raw Cypher code."""


# ── PT-07: Cypher Healing ─────────────────────────────────────────────────────

CYPHER_FIX_USER = """The following Cypher statement failed execution with a Neo4j error.

<broken_cypher>
{broken_cypher}
</broken_cypher>

<neo4j_error>
{error_message}
</neo4j_error>

Fix the Cypher to resolve the error above.

Rules:
- Return ONLY the corrected Cypher. No explanation. No markdown.
- Preserve all MERGE semantics. Do NOT switch to bare CREATE.
- Preserve all parameterised values ($param_name). Do NOT hardcode values.
- Address the EXACT error described. Do not restructure the query unnecessarily."""


# ── PT-08 & PT-09: Answer Generation ─────────────────────────────────────────

ANSWER_SYSTEM = """You are a precise data governance analyst assistant. You answer questions about business concepts and database schemas based strictly on the information provided in the retrieved context.

Rules:
- Answer ONLY from the information in the <retrieved_context> section. Do not use any prior knowledge.
- If the answer is not present in the retrieved context, respond exactly with: "I cannot find this information in the knowledge graph."
- Be concise and direct. Cite the specific concept name or table name from the context when relevant.
- Do not speculate. Do not make assumptions beyond what the context states.
- Format: plain prose. No bullet lists unless the question explicitly asks for a list."""

ANSWER_USER = """Answer the following question using only the retrieved context below.

<retrieved_context>
{context_chunks}
</retrieved_context>

<question>
{user_query}
</question>"""

ANSWER_WITH_CRITIQUE_USER = """Your previous answer contained unsupported claims. A factual audit identified the following problem:

<previous_critique>
{hallucination_critique}
</previous_critique>

You must avoid repeating this mistake. Use ONLY the retrieved context below.

<retrieved_context>
{context_chunks}
</retrieved_context>

<question>
{user_query}
</question>

Generate a corrected answer that addresses the critique above. Stay strictly within the retrieved context."""


# ── PT-10: Hallucination Grader ───────────────────────────────────────────────

GRADER_SYSTEM = """You are a strict factual auditor for AI-generated answers about database schemas and business concepts.

Your task: determine whether a generated answer is fully supported by the provided retrieved context.

Output format:
{
  "grounded": <true | false>,
  "critique": "<specific natural-language critique naming unsupported entities, or null if grounded>",
  "action": "<'pass' | 'regenerate' | 'web_search'>"
}

Action rules:
- "pass": the answer is fully grounded in the retrieved context.
- "regenerate": the answer contains unsupported claims but the context is relevant - the generator should retry with the critique.
- "web_search": the retrieved context is entirely unrelated to the question.

Critique rules (when grounded=false):
- Name the SPECIFIC entity, table, or concept in the answer that is NOT present in the context.
- State WHY: "Table TB_X is not mentioned in any retrieved context chunk."
- Include a correction instruction: "Reformulate the answer omitting TB_X."
- Generic critiques are NOT acceptable.

Output ONLY valid JSON. No markdown. No preamble."""

GRADER_USER = """Audit the following generated answer against the retrieved context.

<retrieved_context>
{context_chunks}
</retrieved_context>

<generated_answer>
{generated_answer}
</generated_answer>

<original_question>
{user_query}
</original_question>

Is every claim in the generated answer supported by the retrieved context? Return the audit JSON."""


# ── Few-Shot Example Banks ────────────────────────────────────────────────────

FEW_SHOT_MAPPING_EXAMPLES: str = """Example 1:
Table: CUSTOMER_MASTER | Columns: CUST_ID (INT, PK), FULL_NAME (VARCHAR), EMAIL (VARCHAR), REGION_CODE (VARCHAR)
-> Concept: "Customer" (confidence: 0.97)
Reasoning: Stores individual customer identity and contact data, directly matching the Customer concept.

Example 2:
Table: TB_PRODUCT | Columns: PRODUCT_ID (INT, PK), SKU (VARCHAR, UNIQUE), PRODUCT_NAME (VARCHAR), UNIT_PRICE (DECIMAL)
-> Concept: "Product" (confidence: 0.95)
Reasoning: SKU, product name, and pricing columns are defining attributes of the Product concept.

Example 3:
Table: SYS_AUDIT_LOG | Columns: LOG_ID (BIGINT, PK), ACTION_TYPE (VARCHAR), TABLE_NAME (VARCHAR), CHANGED_AT (DATETIME)
-> Concept: null (confidence: 0.0)
Reasoning: System audit log - records technical change events only, no business concept counterpart."""

# FEW_SHOT_CYPHER_EXAMPLES is loaded at runtime from the example bank file
# to allow dynamic selection of the most relevant examples per table.
# See src/graph/cypher_generator.py for the selection logic.
```

---

## 5. Tests

```python
"""Unit tests for src/prompts/templates.py"""

from __future__ import annotations

import pytest

from src.prompts import templates


class TestTemplateConstants:
    """Verify all expected constants are present and have required placeholders."""

    # (constant_name, required_placeholders)
    SYSTEM_CONSTANTS = [
        "EXTRACTION_SYSTEM",
        "ER_JUDGE_SYSTEM",
        "MAPPING_SYSTEM",
        "ENRICHMENT_SYSTEM",
        "CRITIC_SYSTEM",
        "CYPHER_SYSTEM",
        "ANSWER_SYSTEM",
        "GRADER_SYSTEM",
    ]
    USER_CONSTANTS_WITH_VARS = [
        ("EXTRACTION_USER", ["chunk_text"]),
        ("ER_JUDGE_USER", ["variants_json", "provenance_json"]),
        ("MAPPING_USER", ["few_shot_examples", "table_ddl", "entities_json"]),
        ("ENRICHMENT_USER", ["table_name", "columns_text"]),
        ("CRITIC_USER", ["proposal_json", "table_ddl", "entities_json"]),
        ("REFLECTION_TEMPLATE", ["role", "output_format", "error_or_critique", "original_input"]),
        ("CYPHER_USER", ["few_shot_examples", "concept_name", "table_ddl"]),
        ("CYPHER_FIX_USER", ["broken_cypher", "error_message"]),
        ("ANSWER_USER", ["context_chunks", "user_query"]),
        ("ANSWER_WITH_CRITIQUE_USER", ["hallucination_critique", "context_chunks", "user_query"]),
        ("GRADER_USER", ["context_chunks", "generated_answer", "user_query"]),
    ]

    def test_all_system_constants_exist(self) -> None:
        for name in self.SYSTEM_CONSTANTS:
            assert hasattr(templates, name), f"Missing: {name}"
            assert isinstance(getattr(templates, name), str)
            assert len(getattr(templates, name)) > 50, f"Too short: {name}"

    def test_all_user_constants_have_placeholders(self) -> None:
        for name, required in self.USER_CONSTANTS_WITH_VARS:
            tmpl = getattr(templates, name)
            for var in required:
                assert f"{{{var}}}" in tmpl, f"Missing placeholder {{{var}}} in {name}"

    def test_few_shot_mapping_examples_not_empty(self) -> None:
        assert len(templates.FEW_SHOT_MAPPING_EXAMPLES) > 100

    def test_few_shot_mapping_examples_contains_all_three_examples(self) -> None:
        fse = templates.FEW_SHOT_MAPPING_EXAMPLES
        assert "CUSTOMER_MASTER" in fse
        assert "TB_PRODUCT" in fse
        assert "SYS_AUDIT_LOG" in fse


class TestTemplateFormatting:
    """Verify templates can be formatted with dummy values without KeyError."""

    def test_extraction_user_format(self) -> None:
        result = templates.EXTRACTION_USER.format(chunk_text="Test passage.")
        assert "Test passage." in result

    def test_reflection_template_format(self) -> None:
        result = templates.REFLECTION_TEMPLATE.format(
            role="Cypher expert",
            output_format="Cypher statement",
            error_or_critique="Syntax error on line 1",
            original_input="MERGE (n:Node)",
        )
        assert "Cypher expert" in result
        assert "Syntax error on line 1" in result

    def test_answer_with_critique_user_format(self) -> None:
        result = templates.ANSWER_WITH_CRITIQUE_USER.format(
            hallucination_critique="TB_X not in context",
            context_chunks="[1] Customer: ...",
            user_query="What is a Customer?",
        )
        assert "TB_X not in context" in result
        assert "What is a Customer?" in result

    def test_cypher_system_bans_bare_create(self) -> None:
        assert "Never use bare CREATE" in templates.CYPHER_SYSTEM

    def test_grader_system_has_all_three_actions(self) -> None:
        for action in ("pass", "regenerate", "web_search"):
            assert action in templates.GRADER_SYSTEM
```

---

## 6. Smoke Test

```bash
python -c "
from src.prompts.templates import (
    EXTRACTION_SYSTEM, EXTRACTION_USER, MAPPING_USER, REFLECTION_TEMPLATE,
    CYPHER_SYSTEM, GRADER_USER, FEW_SHOT_MAPPING_EXAMPLES
)
print('templates.py import OK')
msg = EXTRACTION_USER.format(chunk_text='A Customer is someone who buys things.')
print(f'EXTRACTION_USER format OK ({len(msg)} chars)')
" 2>&1 || echo "Note: run after implementing src/prompts/templates.py"
```
