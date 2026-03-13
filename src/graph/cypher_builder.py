"""Deterministic parameterized Cypher builder for Neo4j upserts.

Generates MERGE-based Cypher with ``$parameter`` placeholders so that all
string values (DDL source, column names, definitions with embedded quotes, etc.)
are handled safely by the Neo4j driver without manual escaping.

This complements the LLM-based :mod:`cypher_generator` (which is used for the
self-reflection demonstration in the thesis) and is used as the actual upsert
executor in the Builder Graph node, making graph writes reliable regardless of
LLM output quality.
"""

from __future__ import annotations

import json

from src.models.schemas import EnrichedTableSchema, MappingProposal

# ── Parameterized MERGE template ─────────────────────────────────────────────

_UPSERT_CYPHER = """\
MERGE (bc:BusinessConcept {name: $concept_name})
ON CREATE SET bc.definition = $concept_definition,
              bc.provenance_text = $provenance_text,
              bc.source_doc = $source_doc,
              bc.synonyms = $synonyms,
              bc.confidence_score = $confidence_score,
              bc.created_at = datetime()
ON MATCH SET  bc.confidence_score = $confidence_score,
              bc.updated_at = datetime()

MERGE (pt:PhysicalTable {table_name: $table_name})
ON CREATE SET pt.schema_name = $schema_name,
              pt.column_names = $column_names,
              pt.column_types = $column_types,
              pt.ddl_source = $ddl_source,
              pt.created_at = datetime()
ON MATCH SET  pt.ddl_source = $ddl_source,
              pt.updated_at = datetime()

MERGE (bc)-[r:MAPPED_TO]->(pt)
ON CREATE SET r.confidence = $confidence,
              r.validated_by = 'llm_judge',
              r.created_at = datetime()
ON MATCH SET  r.confidence = $confidence,
              r.updated_at = datetime()
"""


def build_upsert_cypher(
    proposal: MappingProposal,
    table: EnrichedTableSchema,
) -> tuple[str, dict]:
    """Build a parameterized MERGE Cypher and a params dict.

    Args:
        proposal: The validated :class:`~src.models.schemas.MappingProposal`.
        table:    The :class:`~src.models.schemas.EnrichedTableSchema` for the
                  table being mapped.

    Returns:
        A ``(cypher_template, params)`` tuple ready for
        ``Neo4jClient.execute_cypher(cypher, params)``.
    """
    column_names = [c.name for c in table.columns]
    # Neo4j property values must be primitives or arrays — Map is not supported.
    # Serialize column_types dict as a JSON string for storage.
    column_types = json.dumps({c.name: c.data_type for c in table.columns})

    params: dict = {
        "concept_name": proposal.mapped_concept or "Unknown",
        "concept_definition": proposal.reasoning or "",
        "provenance_text": "",
        "source_doc": "",
        "synonyms": [],
        "confidence_score": proposal.confidence,
        "table_name": table.table_name,
        "schema_name": table.schema_name,
        "column_names": column_names,
        "column_types": column_types,
        "ddl_source": table.ddl_source or "",
        "confidence": proposal.confidence,
    }
    return _UPSERT_CYPHER, params
