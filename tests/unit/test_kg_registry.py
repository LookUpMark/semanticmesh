"""Unit tests for src.graph.kg_registry (SQLite-only, no Neo4j)."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.graph import kg_registry


@pytest.fixture(autouse=True)
def _isolate_db(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Override DB + snapshot paths to use temp directory per test."""
    monkeypatch.setattr(kg_registry, "_REGISTRY_DB", tmp_path / "test_registry.db")
    monkeypatch.setattr(kg_registry, "_SNAPSHOTS_DIR", tmp_path / "snapshots")
    monkeypatch.setattr(kg_registry, "_DATA_DIR", tmp_path)
    yield


def _insert_snapshot(snap_id: str, name: str, tmp_path: Path) -> Path:
    """Helper: manually insert a snapshot into the DB and create the JSON file."""
    (tmp_path / "snapshots").mkdir(exist_ok=True)
    snap_path = tmp_path / "snapshots" / f"{snap_id}.json"
    snap_path.write_text(json.dumps({"id": snap_id, "name": name, "nodes": [], "edges": []}))

    db_path = tmp_path / "test_registry.db"
    conn = sqlite3.connect(str(db_path))
    conn.execute("""
        CREATE TABLE IF NOT EXISTS kg_snapshots (
            id TEXT PRIMARY KEY, name TEXT NOT NULL, description TEXT NOT NULL DEFAULT '',
            created_at TEXT NOT NULL, node_count INTEGER NOT NULL DEFAULT 0,
            edge_count INTEGER NOT NULL DEFAULT 0, snapshot_path TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS kg_active (
            singleton INTEGER PRIMARY KEY DEFAULT 1 CHECK (singleton = 1),
            snapshot_id TEXT REFERENCES kg_snapshots(id) ON DELETE SET NULL
        )
    """)
    conn.execute("INSERT OR IGNORE INTO kg_active (singleton, snapshot_id) VALUES (1, NULL)")
    conn.execute(
        "INSERT INTO kg_snapshots (id, name, description, created_at, node_count, edge_count, snapshot_path) "
        "VALUES (?, ?, '', '2026-01-01T00:00:00', 5, 3, ?)",
        (snap_id, name, str(snap_path)),
    )
    conn.commit()
    conn.close()
    return snap_path


class TestListSnapshots:
    def test_returns_empty_when_no_snapshots(self) -> None:
        result = kg_registry.list_snapshots()
        assert result == []

    def test_returns_snapshot_metadata(self, tmp_path: Path) -> None:
        _insert_snapshot("snap-001", "My KG", tmp_path)
        result = kg_registry.list_snapshots()
        assert len(result) == 1
        assert result[0]["id"] == "snap-001"
        assert result[0]["name"] == "My KG"
        assert result[0]["node_count"] == 5
        assert result[0]["edge_count"] == 3
        assert result[0]["is_active"] is False


class TestGetActiveSnapshot:
    def test_returns_none_when_no_active(self) -> None:
        assert kg_registry.get_active_snapshot() is None

    def test_returns_active_when_set(self, tmp_path: Path) -> None:
        _insert_snapshot("snap-002", "Active KG", tmp_path)
        # Set it active
        db_path = tmp_path / "test_registry.db"
        conn = sqlite3.connect(str(db_path))
        conn.execute("UPDATE kg_active SET snapshot_id = 'snap-002' WHERE singleton = 1")
        conn.commit()
        conn.close()

        result = kg_registry.get_active_snapshot()
        assert result is not None
        assert result["id"] == "snap-002"
        assert result["is_active"] is True


class TestEjectSnapshot:
    def test_clears_active_pointer(self, tmp_path: Path) -> None:
        _insert_snapshot("snap-003", "To Eject", tmp_path)
        db_path = tmp_path / "test_registry.db"
        conn = sqlite3.connect(str(db_path))
        conn.execute("UPDATE kg_active SET snapshot_id = 'snap-003' WHERE singleton = 1")
        conn.commit()
        conn.close()

        kg_registry.eject_snapshot()
        assert kg_registry.get_active_snapshot() is None


class TestDeleteSnapshot:
    def test_removes_file_and_db_entry(self, tmp_path: Path) -> None:
        snap_path = _insert_snapshot("snap-del", "To Delete", tmp_path)
        assert snap_path.exists()

        kg_registry.delete_snapshot("snap-del")

        assert not snap_path.exists()
        assert kg_registry.list_snapshots() == []

    def test_raises_on_not_found(self) -> None:
        with pytest.raises(ValueError, match="not found"):
            kg_registry.delete_snapshot("nonexistent-id")


class TestRenameSnapshot:
    def test_updates_name_and_description(self, tmp_path: Path) -> None:
        _insert_snapshot("snap-ren", "Old Name", tmp_path)
        result = kg_registry.rename_snapshot("snap-ren", "New Name", description="Updated")
        assert result["name"] == "New Name"
        assert result["description"] == "Updated"

    def test_keeps_description_when_none(self, tmp_path: Path) -> None:
        _insert_snapshot("snap-ren2", "Original", tmp_path)
        result = kg_registry.rename_snapshot("snap-ren2", "Renamed")
        assert result["name"] == "Renamed"
        assert result["description"] == ""  # original was empty

    def test_raises_on_not_found(self) -> None:
        with pytest.raises(ValueError, match="not found"):
            kg_registry.rename_snapshot("nope", "Whatever")


class TestSaveSnapshot:
    @patch("src.graph.kg_registry._export_graph")
    def test_creates_file_and_registry_entry(self, mock_export: MagicMock, tmp_path: Path) -> None:
        mock_export.return_value = (
            [{"eid": "1", "labels": ["BusinessConcept"], "props": {"name": "Order"}}],
            [],
        )
        result = kg_registry.save_snapshot("Test Save", description="desc")
        assert result["name"] == "Test Save"
        assert result["node_count"] == 1
        assert result["edge_count"] == 0

        # Verify file exists
        snaps = list((tmp_path / "snapshots").glob("*.json"))
        assert len(snaps) == 1


class TestLoadSnapshot:
    @patch("src.graph.kg_registry._import_graph")
    def test_loads_and_sets_active(self, mock_import: MagicMock, tmp_path: Path) -> None:
        _insert_snapshot("snap-load", "To Load", tmp_path)
        result = kg_registry.load_snapshot("snap-load")
        assert result["is_active"] is True
        mock_import.assert_called_once()

    def test_raises_on_not_found(self) -> None:
        with pytest.raises(ValueError, match="not found"):
            kg_registry.load_snapshot("missing-id")
