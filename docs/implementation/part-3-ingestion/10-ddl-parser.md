# Part 3 — `src/ingestion/ddl_parser.py`

## 1. Purpose & Context

**Epic:** EP-05 DDL Schema Parsing  
**US-05-01** — DDL Parser

Converts raw SQL DDL text into structured `TableSchema` objects using the `sqlglot` library. Fully deterministic — no LLM call. Supports MySQL, PostgreSQL, T-SQL, and Oracle dialects. The output feeds directly into the Schema Enrichment node and then the RAG Mapping node.

---

## 2. Prerequisites

- `src/models/schemas.py` — `ColumnSchema`, `TableSchema` (step 3)
- `src/config/logging.py` — `get_logger`
- Dependencies: `sqlglot>=23`

---

## 3. Public API

| Symbol | Signature | Description |
|---|---|---|
| `DDLParseError` | `class(Exception)` | Raised on unparseable DDL input |
| `parse_ddl` | `(ddl_text: str, dialect: str = "mysql") -> list[TableSchema]` | Parses all CREATE TABLE statements found in `ddl_text` |
| `parse_ddl_file` | `(path: Path, dialect: str = "mysql") -> list[TableSchema]` | Convenience: reads file → `parse_ddl` |

---

## 4. Full Implementation

```python
"""Deterministic SQL DDL parser using sqlglot.

EP-05: Converts raw SQL DDL text into structured TableSchema objects.
No LLM involved. Supports mysql, postgres, tsql, oracle dialects.
"""

from __future__ import annotations

import logging
import re
from pathlib import Path

import sqlglot
import sqlglot.expressions as exp

from src.config.logging import get_logger
from src.models.schemas import ColumnSchema, TableSchema

logger: logging.Logger = get_logger(__name__)


class DDLParseError(Exception):
    """Raised when DDL cannot be parsed into at least one TableSchema."""


def _normalise_type(data_type: str) -> str:
    """Strip length/precision details for cleaner stored types.

    Examples:
        "VARCHAR(200)" → "VARCHAR"
        "DECIMAL(10,2)" → "DECIMAL"
        "BIGINT" → "BIGINT"
    """
    return re.sub(r"\(.*\)", "", data_type).strip().upper()


def _extract_table(create_expr: exp.Create, ddl_source: str) -> TableSchema | None:
    """Extract a single TableSchema from a parsed CREATE TABLE expression.

    Returns None if the expression is not a CREATE TABLE or has no columns.
    """
    # Only handle CREATE TABLE (not CREATE INDEX, VIEW, etc.)
    if create_expr.args.get("kind", "").upper() != "TABLE":
        return None

    table_ref = create_expr.find(exp.Table)
    if table_ref is None:
        return None

    table_name: str = table_ref.name.upper()
    schema_name: str | None = table_ref.db.upper() if table_ref.db else None

    # Collect all primary key column names declared inline or via table constraint
    pk_columns: set[str] = set()
    schema_def = create_expr.find(exp.Schema)
    if schema_def is None:
        return None

    for constraint in schema_def.find_all(exp.PrimaryKey):
        for col in constraint.find_all(exp.Column):
            pk_columns.add(col.name.upper())

    # Build ColumnSchema list
    columns: list[ColumnSchema] = []
    for col_def in schema_def.find_all(exp.ColumnDef):
        col_name = col_def.name.upper()
        data_type_expr = col_def.find(exp.DataType)
        data_type = _normalise_type(str(data_type_expr)) if data_type_expr else "UNKNOWN"

        is_pk = col_name in pk_columns
        is_fk = False
        references: str | None = None

        # Inline PRIMARY KEY constraint
        for constraint in col_def.find_all(exp.ColumnConstraint):
            kind = constraint.args.get("kind")
            if isinstance(kind, exp.PrimaryKeyColumnConstraint):
                is_pk = True
            if isinstance(kind, exp.Reference):
                is_fk = True
                ref_table = kind.find(exp.Table)
                ref_col = kind.find(exp.Column)
                if ref_table and ref_col:
                    references = f"{ref_table.name.upper()}.{ref_col.name.upper()}"

        columns.append(
            ColumnSchema(
                name=col_name,
                data_type=data_type,
                is_primary_key=is_pk,
                is_foreign_key=is_fk,
                references=references,
            )
        )

    # Table-level FOREIGN KEY constraints
    for fk_constraint in schema_def.find_all(exp.ForeignKey):
        fk_cols = [c.name.upper() for c in fk_constraint.find_all(exp.Column)]
        reference = fk_constraint.find(exp.Reference)
        if reference:
            ref_table = reference.find(exp.Table)
            ref_cols = [c.name.upper() for c in reference.find_all(exp.Column)]
            for i, fk_col_name in enumerate(fk_cols):
                for col in columns:
                    if col.name == fk_col_name:
                        col.is_foreign_key = True
                        if ref_table and i < len(ref_cols):
                            col.references = f"{ref_table.name.upper()}.{ref_cols[i]}"

    if not columns:
        logger.warning("Table '%s' has no parseable columns — skipping.", table_name)
        return None

    return TableSchema(
        table_name=table_name,
        schema_name=schema_name,
        columns=columns,
        ddl_source=ddl_source,
    )


def parse_ddl(ddl_text: str, dialect: str = "mysql") -> list[TableSchema]:
    """Parse all CREATE TABLE statements in a DDL text block.

    Args:
        ddl_text: Raw SQL DDL containing one or more CREATE TABLE statements.
        dialect: sqlglot dialect for parsing. Options: "mysql", "postgres",
                 "tsql", "oracle". Defaults to "mysql" (most permissive).

    Returns:
        List of ``TableSchema`` objects, one per CREATE TABLE statement found.

    Raises:
        DDLParseError: If no CREATE TABLE statements could be parsed.
    """
    try:
        statements = sqlglot.parse(ddl_text, dialect=dialect, error_level=sqlglot.ErrorLevel.WARN)
    except Exception as exc:
        raise DDLParseError(f"sqlglot failed to tokenise DDL: {exc}") from exc

    tables: list[TableSchema] = []
    for stmt in statements:
        if stmt is None:
            continue
        if not isinstance(stmt, exp.Create):
            continue
        # Use the statement's own SQL string as ddl_source
        table_ddl_source = stmt.sql(dialect=dialect)
        schema = _extract_table(stmt, ddl_source=table_ddl_source)
        if schema is not None:
            tables.append(schema)
            logger.debug("Parsed table '%s' (%d columns)", schema.table_name, len(schema.columns))

    if not tables:
        raise DDLParseError("No CREATE TABLE statements could be parsed from the input DDL.")

    logger.info("Parsed %d table(s) from DDL input.", len(tables))
    return tables


def parse_ddl_file(path: Path, dialect: str = "mysql") -> list[TableSchema]:
    """Load a .sql file and parse it with ``parse_ddl``.

    Args:
        path: Path to the SQL file.
        dialect: sqlglot dialect.

    Returns:
        List of ``TableSchema`` objects.

    Raises:
        FileNotFoundError: If the file does not exist.
        DDLParseError: propagated from ``parse_ddl``.
    """
    if not path.exists():
        raise FileNotFoundError(f"DDL file not found: {path}")
    ddl_text = path.read_text(encoding="utf-8")
    return parse_ddl(ddl_text, dialect=dialect)
```

---

## 5. Tests

```python
"""Unit tests for src/ingestion/ddl_parser.py — UT-03"""

from __future__ import annotations

from pathlib import Path

import pytest

from src.ingestion.ddl_parser import DDLParseError, parse_ddl, parse_ddl_file
from src.models.schemas import TableSchema

# ── Shared DDL fixtures ───────────────────────────────────────────────────────

SIMPLE_DDL = """
CREATE TABLE CUSTOMER_MASTER (
    CUST_ID     INT PRIMARY KEY,
    FULL_NAME   VARCHAR(200) NOT NULL,
    EMAIL       VARCHAR(150) UNIQUE,
    REGION_CODE VARCHAR(10),
    CREATED_AT  DATETIME DEFAULT CURRENT_TIMESTAMP
);
"""

FK_DDL = """
CREATE TABLE CUSTOMER_MASTER (
    CUST_ID   INT PRIMARY KEY,
    FULL_NAME VARCHAR(200)
);

CREATE TABLE SALES_ORDER_HDR (
    ORDER_ID BIGINT PRIMARY KEY,
    CUST_ID  INT NOT NULL,
    ORDER_DATE DATE,
    CONSTRAINT fk_order_customer FOREIGN KEY (CUST_ID) REFERENCES CUSTOMER_MASTER(CUST_ID)
);
"""

POSTGRES_DDL = """
CREATE TABLE public.tb_product (
    product_id SERIAL PRIMARY KEY,
    sku        VARCHAR(50) UNIQUE NOT NULL,
    unit_price NUMERIC(10,2)
);
"""


# ── parse_ddl basic ───────────────────────────────────────────────────────────

class TestParseDdlBasic:
    def test_parses_single_table(self) -> None:
        tables = parse_ddl(SIMPLE_DDL)
        assert len(tables) == 1
        assert tables[0].table_name == "CUSTOMER_MASTER"

    def test_returns_correct_column_count(self) -> None:
        tables = parse_ddl(SIMPLE_DDL)
        assert len(tables[0].columns) == 5

    def test_primary_key_detected(self) -> None:
        tables = parse_ddl(SIMPLE_DDL)
        pk_cols = [c for c in tables[0].columns if c.is_primary_key]
        assert len(pk_cols) == 1
        assert pk_cols[0].name == "CUST_ID"

    def test_data_type_normalised(self) -> None:
        tables = parse_ddl(SIMPLE_DDL)
        full_name_col = next(c for c in tables[0].columns if c.name == "FULL_NAME")
        assert full_name_col.data_type == "VARCHAR"

    def test_ddl_source_preserved(self) -> None:
        tables = parse_ddl(SIMPLE_DDL)
        assert "CUSTOMER_MASTER" in tables[0].ddl_source


class TestParseDdlMultipleTables:
    def test_parses_two_tables(self) -> None:
        tables = parse_ddl(FK_DDL)
        assert len(tables) == 2

    def test_foreign_key_detected(self) -> None:
        tables = parse_ddl(FK_DDL)
        order_table = next(t for t in tables if "ORDER" in t.table_name)
        fk_cols = [c for c in order_table.columns if c.is_foreign_key]
        assert len(fk_cols) >= 1
        assert fk_cols[0].name == "CUST_ID"

    def test_fk_references_correct_table(self) -> None:
        tables = parse_ddl(FK_DDL)
        order_table = next(t for t in tables if "ORDER" in t.table_name)
        cust_id_col = next(c for c in order_table.columns if c.name == "CUST_ID")
        assert cust_id_col.references is not None
        assert "CUSTOMER_MASTER" in cust_id_col.references


class TestParseDdlDialects:
    def test_postgres_dialect(self) -> None:
        tables = parse_ddl(POSTGRES_DDL, dialect="postgres")
        assert len(tables) == 1
        assert tables[0].table_name.upper() == "TB_PRODUCT"
        assert tables[0].schema_name is not None


class TestParseDdlErrorCases:
    def test_empty_string_raises(self) -> None:
        with pytest.raises(DDLParseError):
            parse_ddl("")

    def test_no_create_table_raises(self) -> None:
        with pytest.raises(DDLParseError):
            parse_ddl("SELECT * FROM customers WHERE id = 1;")

    def test_only_whitespace_raises(self) -> None:
        with pytest.raises(DDLParseError):
            parse_ddl("   \n\n   ")


# ── parse_ddl_file ────────────────────────────────────────────────────────────

class TestParseDdlFile:
    def test_parses_simple_schema_fixture(self) -> None:
        path = Path("tests/fixtures/sample_ddl/simple_schema.sql")
        tables = parse_ddl_file(path)
        assert len(tables) >= 1
        table_names = {t.table_name for t in tables}
        assert "CUSTOMER_MASTER" in table_names

    def test_raises_on_missing_file(self, tmp_path: Path) -> None:
        with pytest.raises(FileNotFoundError):
            parse_ddl_file(tmp_path / "nonexistent.sql")
```

---

## 6. Smoke Test

```bash
python -c "
from pathlib import Path
from src.ingestion.ddl_parser import parse_ddl_file
tables = parse_ddl_file(Path('tests/fixtures/sample_ddl/simple_schema.sql'))
for t in tables:
    print(f'{t.table_name}: {[c.name for c in t.columns]}')
"
```
