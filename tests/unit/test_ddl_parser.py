"""Unit tests for src/ingestion/ddl_parser.py — UT-03"""

from __future__ import annotations

from pathlib import Path

import pytest

from src.ingestion.ddl_parser import DDLParseError, parse_ddl, parse_ddl_file

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
        path = (
            Path(__file__).resolve().parent.parent
            / "fixtures"
            / "01_basics_ecommerce"
            / "schema.sql"
        )
        tables = parse_ddl_file(path)
        assert len(tables) >= 1
        table_names = {t.table_name for t in tables}
        assert "CUSTOMER_MASTER" in table_names

    def test_raises_on_missing_file(self, tmp_path: Path) -> None:
        with pytest.raises(FileNotFoundError):
            parse_ddl_file(tmp_path / "nonexistent.sql")
