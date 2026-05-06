"""Unit tests for src.ingestion.file_registry."""

from __future__ import annotations

import tempfile
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from src.ingestion.file_registry import (
    check_file_status,
    compute_file_sha,
    get_orphaned_files,
    purge_file_data,
    register_file,
)


class TestComputeFileSha:
    def test_produces_64_char_hex(self, tmp_path: Path) -> None:
        f = tmp_path / "test.txt"
        f.write_text("hello world")
        sha = compute_file_sha(f)
        assert len(sha) == 64
        assert all(c in "0123456789abcdef" for c in sha)

    def test_same_content_same_hash(self, tmp_path: Path) -> None:
        f1 = tmp_path / "a.txt"
        f2 = tmp_path / "b.txt"
        content = "identical content"
        f1.write_text(content)
        f2.write_text(content)
        assert compute_file_sha(f1) == compute_file_sha(f2)

    def test_different_content_different_hash(self, tmp_path: Path) -> None:
        f1 = tmp_path / "a.txt"
        f2 = tmp_path / "b.txt"
        f1.write_text("alpha")
        f2.write_text("beta")
        assert compute_file_sha(f1) != compute_file_sha(f2)

    def test_raises_on_missing_file(self) -> None:
        with pytest.raises(FileNotFoundError):
            compute_file_sha("/nonexistent/path/file.txt")


class TestCheckFileStatus:
    def test_returns_new_when_no_node(self) -> None:
        client = MagicMock()
        client.execute_cypher.return_value = []
        assert check_file_status(client, "/path/to/doc.txt", "abc123") == "new"

    def test_returns_unchanged_when_sha_matches(self) -> None:
        client = MagicMock()
        client.execute_cypher.return_value = [{"sha": "abc123"}]
        assert check_file_status(client, "/path/to/doc.txt", "abc123") == "unchanged"

    def test_returns_modified_when_sha_differs(self) -> None:
        client = MagicMock()
        client.execute_cypher.return_value = [{"sha": "old_sha"}]
        assert check_file_status(client, "/path/to/doc.txt", "new_sha") == "modified"


class TestRegisterFile:
    def test_calls_execute_cypher(self, tmp_path: Path) -> None:
        f = tmp_path / "doc.txt"
        f.write_text("content")
        client = MagicMock()
        register_file(client, str(f), "sha256hex", chunk_count=5)
        client.execute_cypher.assert_called_once()
        args = client.execute_cypher.call_args
        assert "MERGE" in args[0][0]
        assert args[0][1]["chunk_count"] == 5


class TestGetOrphanedFiles:
    def test_returns_paths_not_in_current_set(self) -> None:
        client = MagicMock()
        client.execute_cypher.return_value = [
            {"path": "/old/file1.txt"},
            {"path": "/old/file2.txt"},
        ]
        orphans = get_orphaned_files(client, {"/current/file3.txt"})
        assert "/old/file1.txt" in orphans
        assert "/old/file2.txt" in orphans

    def test_returns_empty_when_no_orphans(self) -> None:
        client = MagicMock()
        client.execute_cypher.return_value = []
        orphans = get_orphaned_files(client, {"/a.txt", "/b.txt"})
        assert orphans == []

    def test_returns_empty_on_empty_current_paths(self) -> None:
        client = MagicMock()
        orphans = get_orphaned_files(client, set())
        assert orphans == []
        client.execute_cypher.assert_not_called()


class TestPurgeFileData:
    def test_returns_total_deleted_count(self) -> None:
        client = MagicMock()
        # Chunk, ParentChunk, PhysicalTable, BusinessConcept responses
        client.execute_cypher.side_effect = [
            [{"n": 5}],   # Chunks
            [{"n": 2}],   # ParentChunks
            [{"n": 1}],   # PhysicalTables
            None,          # SourceFile deletion (no RETURN)
            [{"n": 3}],   # Orphan BusinessConcepts
        ]
        total = purge_file_data(client, "tests/fixtures/doc.txt")
        assert total == 5 + 2 + 1 + 3
