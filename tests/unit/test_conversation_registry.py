"""Unit tests for src.graph.conversation_registry."""

from __future__ import annotations

from pathlib import Path

import pytest

from src.graph import conversation_registry


@pytest.fixture(autouse=True)
def _isolate_db(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Override DB paths to use temp directory per test."""
    monkeypatch.setattr(conversation_registry, "_REGISTRY_DB", tmp_path / "test_conv.db")
    monkeypatch.setattr(conversation_registry, "_DATA_DIR", tmp_path)
    yield


class TestListConversations:
    def test_returns_empty_initially(self) -> None:
        assert conversation_registry.list_conversations() == []

    def test_returns_saved_conversations(self) -> None:
        conversation_registry.save_conversation(
            session_id="sess-1",
            title="Test Chat",
            messages=[{"role": "user", "content": "Hello"}],
        )
        result = conversation_registry.list_conversations()
        assert len(result) == 1
        assert result[0]["title"] == "Test Chat"
        assert result[0]["message_count"] == 1


class TestSaveConversation:
    def test_saves_and_returns_metadata(self) -> None:
        msgs = [
            {"role": "user", "content": "What is an order?"},
            {"role": "assistant", "content": "An order is a purchase transaction."},
        ]
        result = conversation_registry.save_conversation(
            session_id="sess-2",
            title="Order Question",
            messages=msgs,
        )
        assert result["title"] == "Order Question"
        assert result["message_count"] == 2
        assert result["session_id"] == "sess-2"

    def test_auto_title_from_first_user_message(self) -> None:
        msgs = [{"role": "user", "content": "How are products stored?"}]
        result = conversation_registry.save_conversation(
            session_id="sess-3",
            title="",
            messages=msgs,
        )
        assert "products" in result["title"].lower()

    def test_stores_active_snapshot_id(self) -> None:
        result = conversation_registry.save_conversation(
            session_id="sess-4",
            title="With Snapshot",
            messages=[{"role": "user", "content": "test"}],
            active_snapshot_id="snap-123",
        )
        assert result["active_snapshot_id"] == "snap-123"


class TestGetConversation:
    def test_returns_full_conversation_with_messages(self) -> None:
        msgs = [{"role": "user", "content": "Hi"}, {"role": "assistant", "content": "Hello!"}]
        saved = conversation_registry.save_conversation(
            session_id="sess-5", title="Full", messages=msgs
        )
        result = conversation_registry.get_conversation(saved["id"])
        assert result["messages"] == msgs
        assert result["title"] == "Full"

    def test_raises_on_not_found(self) -> None:
        with pytest.raises(ValueError, match="not found"):
            conversation_registry.get_conversation("nonexistent-id")


class TestRenameConversation:
    def test_updates_title(self) -> None:
        saved = conversation_registry.save_conversation(
            session_id="sess-6", title="Old Title", messages=[{"role": "user", "content": "x"}]
        )
        result = conversation_registry.rename_conversation(saved["id"], "New Title")
        assert result["title"] == "New Title"

    def test_raises_on_not_found(self) -> None:
        with pytest.raises(ValueError, match="not found"):
            conversation_registry.rename_conversation("nope", "Whatever")


class TestDeleteConversation:
    def test_removes_conversation(self) -> None:
        saved = conversation_registry.save_conversation(
            session_id="sess-7", title="To Delete", messages=[{"role": "user", "content": "y"}]
        )
        conversation_registry.delete_conversation(saved["id"])
        assert conversation_registry.list_conversations() == []

    def test_raises_on_not_found(self) -> None:
        with pytest.raises(ValueError, match="not found"):
            conversation_registry.delete_conversation("missing-id")
