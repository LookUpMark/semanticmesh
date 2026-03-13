# Part 6 — `src/graph/cypher_builder.py`

## 1. Purpose & Context

**Epic:** EP-10 / EP-11 Cypher Pipeline Hardening  
**Step 22b** — Deterministic Parameterized Cypher Builder (fallback path)

`cypher_builder` provides a **guaranteed-safe fallback** for the graph-write step of the ingestion pipeline. When the LLM-generated Cypher cannot be healed after exhausting all repair attempts (`cypher_failed=True`), `_node_build_graph` in `builder_graph.py` calls `build_upsert_cypher` instead of executing LLM output directly.

### Why parameterized queries?

LLMs embedding string values inline into Cypher produce brittle output. A DDL source string with embedded single quotes, backslashes, or multi-line text will break any hand-rolled escaping strategy — and the LLM rarely applies escaping consistently. The root cause is that **value escaping and query structure are conflated** when the LLM writes both at once.

`cypher_builder` separates those concerns entirely:

- The **Cypher template** (`_UPSERT_CYPHER`) is a fixed string with `$param` placeholders — it never changes.
- All **values** (including DDL source strings with embedded quotes) are passed as driver-bound parameters.
- The **Neo4j driver** handles all escaping via parameter binding — values never touch the query string.

This is functionally equivalent to a prepared statement and eliminates the entire class of quoting and injection bugs.

### Position in `_node_build_graph`

```
_node_build_graph
│
├── cypher_failed=False → execute LLM-healed Cypher (primary path)
│
└── cypher_failed=True  → build_upsert_cypher(proposal, table)
                          ↳ fixed MERGE template + params dict
                          ↳ passed to Neo4jClient.execute_cypher (fallback path)
```

---

## 2. Prerequisites

| Dependency | Role |
|---|---|
| `src/models/schemas.py` | Provides `MappingProposal` and `EnrichedTableSchema` — the two input types |
| `src/graph/builder_graph.py` | The LangGraph node that calls `build_upsert_cypher` when `cypher_failed=True` |
| `src/graph/neo4j_client.py` | `Neo4jClient.execute_cypher` receives the `(cypher, params)` tuple returned by this module |

No third-party packages are required beyond the standard library — this module is intentionally dependency-free.

---

## 3. Public API

| Symbol | Signature | Description |
|---|---|---|
| `build_upsert_cypher` | `(proposal: MappingProposal, table: EnrichedTableSchema) -> tuple[str, dict]` | Returns the fixed MERGE Cypher template and a fully-populated params dict ready for driver execution |
| `build_fk_cypher` | `(table: TableSchema) -> list[tuple[str, dict]]` | Returns a list of `(cypher, params)` tuples — one per FK column — that create `:REFERENCES` edges between `PhysicalTable` nodes |

The returned tuple is consumed directly by `Neo4jClient.execute_cypher`:

```python
cypher, params = build_upsert_cypher(proposal, table)
client.execute_cypher(cypher, params)
```

### Cypher template produced

The fixed template performs idempotent upserts on three graph elements, with `datetime()` timestamps managed server-side:

| Graph element | Operation | Key property |
|---|---|---|
| `(bc:BusinessConcept)` | `MERGE` | `name` |
| `(pt:PhysicalTable)` | `MERGE` | `table_name` |
| `(bc)-[r:MAPPED_TO]->(pt)` | `MERGE` | — (implicit by node pair) |

### Parameters bound by the driver

| Parameter | Source |
|---|---|
| `$concept_name` | `proposal.mapped_concept` (falls back to `"Unknown"`) |
| `$concept_definition` | `proposal.reasoning` |
| `$provenance_text` | `""` (reserved for future enrichment) |
| `$source_doc` | `""` (reserved for future enrichment) |
| `$synonyms` | `[]` (reserved for future enrichment) |
| `$confidence_score` | `proposal.confidence` |
| `$table_name` | `table.table_name` |
| `$schema_name` | `table.schema_name` |
| `$column_names` | `[col.name for col in table.columns]` |
| `$column_types` | `{col.name: col.data_type for col in table.columns}` |
| `$ddl_source` | `table.ddl_source` |
| `$confidence` | `proposal.confidence` (used on the `MAPPED_TO` relationship) |

> **Note:** `$provenance_text`, `$source_doc`, and `$synonyms` are set to empty defaults today. They exist in the template to keep the schema stable for future enrichment steps without requiring a template change.

---

## 4. Full Implementation

```python
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
    column_types = {c.name: c.data_type for c in table.columns}

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
```

---

### `build_fk_cypher`

Builds `MERGE` Cypher statements for foreign-key edges between `PhysicalTable` nodes. Called by `_node_build_graph` in `builder_graph.py` immediately after the main upsert, for every table that declares FK columns.

#### Cypher template produced

```cypher
MERGE (src:PhysicalTable {name: $src_name})
MERGE (tgt:PhysicalTable {name: $tgt_name})
MERGE (src)-[r:REFERENCES {fk_column: $fk_col, ref_column: $ref_col}]->(tgt)
```

The `MERGE` on the target node creates a **stub** `PhysicalTable` if the referenced table has not been ingested yet — allowing FK relationships to be recorded before the full schema of the referenced table is loaded. The stub is promoted to a full node when that table is eventually upserted.

#### Parameters bound by the driver

| Parameter | Source |
|---|---|
| `$src_name` | `table.table_name` (the table that declares the FK) |
| `$tgt_name` | `column.foreign_key.referenced_table` |
| `$fk_col` | `column.name` (the FK column in the source table) |
| `$ref_col` | `column.foreign_key.referenced_column` |

#### Implementation

```python
_FK_CYPHER = """\
MERGE (src:PhysicalTable {name: $src_name})
MERGE (tgt:PhysicalTable {name: $tgt_name})
MERGE (src)-[r:REFERENCES {fk_column: $fk_col, ref_column: $ref_col}]->(tgt)
"""


def build_fk_cypher(table: TableSchema) -> list[tuple[str, dict]]:
    """Build MERGE Cypher for FK edges: (:PhysicalTable)-[:REFERENCES]->(:PhysicalTable).

    Iterates ``table.columns`` and emits one ``(cypher, params)`` tuple for each
    column whose ``foreign_key`` field is not ``None``.  Returns an empty list
    when the table has no FK columns, so the caller can skip the Neo4j round-trip
    entirely.

    The target ``PhysicalTable`` node is created as a stub if it does not yet
    exist — the stub is promoted when the referenced table is eventually upserted.

    Args:
        table: Parsed :class:`~src.models.schemas.TableSchema` with column
               metadata including optional ``foreign_key`` descriptors.

    Returns:
        A list of ``(cypher_template, params)`` tuples — one per FK column —
        ready for ``Neo4jClient.execute_cypher(cypher, params)``.
        Returns ``[]`` if no FK columns are present.

    Used by:
        ``_node_build_graph`` in ``builder_graph.py`` after the main upsert.
    """
    result: list[tuple[str, dict]] = []
    for col in table.columns:
        if col.foreign_key is None:
            continue
        params = {
            "src_name": table.table_name,
            "tgt_name": col.foreign_key.referenced_table,
            "fk_col": col.name,
            "ref_col": col.foreign_key.referenced_column,
        }
        result.append((_FK_CYPHER, params))
    return result
```

---

## 5. Tests

```python
"""Unit tests for src/graph/cypher_builder.py — UT-22b"""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from src.graph.cypher_builder import build_upsert_cypher


# ── Helpers ────────────────────────────────────────────────────────────────────

def _make_column(name: str, data_type: str) -> MagicMock:
    col = MagicMock()
    col.name = name
    col.data_type = data_type
    return col


def _make_proposal(
    mapped_concept: str | None = "Customer",
    confidence: float = 0.92,
    reasoning: str = "Strong structural match.",
    table_name: str = "CUSTOMER",
) -> MagicMock:
    """Return a minimal MappingProposal mock."""
    proposal = MagicMock()
    proposal.mapped_concept = mapped_concept
    proposal.confidence = confidence
    proposal.reasoning = reasoning
    proposal.table_name = table_name
    return proposal


def _make_table(
    table_name: str = "CUSTOMER",
    schema_name: str | None = "dbo",
    columns: list | None = None,
    ddl_source: str = "CREATE TABLE CUSTOMER (id INT PRIMARY KEY)",
) -> MagicMock:
    """Return a minimal EnrichedTableSchema mock."""
    table = MagicMock()
    table.table_name = table_name
    table.schema_name = schema_name
    table.columns = columns if columns is not None else [
        _make_column("id", "INT"),
        _make_column("name", "VARCHAR(100)"),
    ]
    table.ddl_source = ddl_source
    return table


# ── (a) Return-type contract ───────────────────────────────────────────────────

class TestReturnType:
    def test_returns_tuple_of_str_and_dict(self) -> None:
        result = build_upsert_cypher(_make_proposal(), _make_table())
        assert isinstance(result, tuple)
        assert len(result) == 2
        cypher, params = result
        assert isinstance(cypher, str)
        assert isinstance(params, dict)


# ── (b) concept_name matches proposal.mapped_concept ─────────────────────────

class TestConceptName:
    def test_concept_name_matches_proposal(self) -> None:
        proposal = _make_proposal(mapped_concept="Order")
        _, params = build_upsert_cypher(proposal, _make_table())
        assert params["concept_name"] == "Order"

    def test_none_mapped_concept_falls_back_to_unknown(self) -> None:
        proposal = _make_proposal(mapped_concept=None)
        _, params = build_upsert_cypher(proposal, _make_table())
        assert params["concept_name"] == "Unknown"

    def test_empty_string_mapped_concept_falls_back_to_unknown(self) -> None:
        proposal = _make_proposal(mapped_concept="")
        _, params = build_upsert_cypher(proposal, _make_table())
        assert params["concept_name"] == "Unknown"


# ── (c) column_types dict built from table.columns ───────────────────────────

class TestColumnTypes:
    def test_column_types_dict_built_from_table_columns(self) -> None:
        columns = [
            _make_column("customer_id", "INT"),
            _make_column("email", "VARCHAR(255)"),
            _make_column("created_at", "TIMESTAMP"),
        ]
        _, params = build_upsert_cypher(_make_proposal(), _make_table(columns=columns))
        assert params["column_types"] == {
            "customer_id": "INT",
            "email": "VARCHAR(255)",
            "created_at": "TIMESTAMP",
        }

    def test_column_names_list_matches_columns(self) -> None:
        columns = [_make_column("id", "INT"), _make_column("email", "TEXT")]
        _, params = build_upsert_cypher(_make_proposal(), _make_table(columns=columns))
        assert params["column_names"] == ["id", "email"]

    def test_empty_columns_produces_empty_structures(self) -> None:
        _, params = build_upsert_cypher(_make_proposal(), _make_table(columns=[]))
        assert params["column_types"] == {}
        assert params["column_names"] == []


# ── (d) confidence matches proposal.confidence ────────────────────────────────

class TestConfidence:
    def test_confidence_score_matches_proposal(self) -> None:
        proposal = _make_proposal(confidence=0.75)
        _, params = build_upsert_cypher(proposal, _make_table())
        assert params["confidence_score"] == pytest.approx(0.75)

    def test_relationship_confidence_matches_proposal(self) -> None:
        proposal = _make_proposal(confidence=0.75)
        _, params = build_upsert_cypher(proposal, _make_table())
        assert params["confidence"] == pytest.approx(0.75)

    @pytest.mark.parametrize("conf", [0.0, 0.5, 1.0])
    def test_confidence_boundary_values(self, conf: float) -> None:
        proposal = _make_proposal(confidence=conf)
        _, params = build_upsert_cypher(proposal, _make_table())
        assert params["confidence_score"] == pytest.approx(conf)
        assert params["confidence"] == pytest.approx(conf)


# ── Cypher template integrity ─────────────────────────────────────────────────

class TestCypherTemplate:
    def test_cypher_contains_merge_business_concept(self) -> None:
        cypher, _ = build_upsert_cypher(_make_proposal(), _make_table())
        assert "MERGE (bc:BusinessConcept" in cypher

    def test_cypher_contains_merge_physical_table(self) -> None:
        cypher, _ = build_upsert_cypher(_make_proposal(), _make_table())
        assert "MERGE (pt:PhysicalTable" in cypher

    def test_cypher_contains_mapped_to_relationship(self) -> None:
        cypher, _ = build_upsert_cypher(_make_proposal(), _make_table())
        assert "MAPPED_TO" in cypher

    def test_cypher_uses_dollar_placeholders_only(self) -> None:
        """Raw string values must never appear inline in the Cypher template."""
        proposal = _make_proposal(mapped_concept="Concept with 'quotes'")
        table = _make_table(ddl_source="CREATE TABLE t (x INT -- tricky 'DDL')")
        cypher, _ = build_upsert_cypher(proposal, table)
        assert "Concept with" not in cypher
        assert "tricky" not in cypher
```

---

## 6. Smoke Test

```bash
python -c "
from unittest.mock import MagicMock

from src.graph.cypher_builder import build_upsert_cypher

# Build minimal mock inputs
proposal = MagicMock()
proposal.mapped_concept = 'Customer'
proposal.confidence     = 0.9
proposal.reasoning      = 'Strong match.'
proposal.table_name     = 'CUSTOMER'

col = MagicMock()
col.name      = 'CUST_ID'
col.data_type = 'INT'

table = MagicMock()
table.table_name  = 'CUSTOMER'
table.schema_name = 'dbo'
table.columns     = [col]
table.ddl_source  = 'CREATE TABLE CUSTOMER (CUST_ID INT PRIMARY KEY)'

cypher, params = build_upsert_cypher(proposal, table)

print('=== Cypher template ===')
print(cypher)
print('=== Params ===')
for k, v in params.items():
    print(f'  {k}: {v!r}')

assert isinstance(cypher, str), 'Expected str'
assert isinstance(params, dict), 'Expected dict'
assert params['concept_name'] == 'Customer'
assert params['column_types'] == {'CUST_ID': 'INT'}
assert params['column_names'] == ['CUST_ID']
assert params['confidence_score'] == 0.9
assert params['confidence'] == 0.9
print()
print('Smoke test PASSED.')
"
```
