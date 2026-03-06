"""Unit tests for src/ingestion/pdf_loader.py — UT-02"""

from __future__ import annotations

from typing import TYPE_CHECKING
from unittest.mock import MagicMock, patch

import pytest

from src.ingestion.pdf_loader import (
    IngestionError,
    chunk_documents,
    load_and_chunk_pdf,
    load_pdf,
)
from src.models.schemas import Chunk, Document

if TYPE_CHECKING:
    from pathlib import Path

# ── Fixtures ───────────────────────────────────────────────────────────────────

def _make_document(text: str, page: int = 1, source: str = "test.pdf") -> Document:
    return Document(text=text, metadata={"source": source, "page": str(page)})


# ── load_pdf ──────────────────────────────────────────────────────────────────

class TestLoadPdf:
    def test_file_not_found_raises(self, tmp_path: Path) -> None:
        with pytest.raises(IngestionError, match="not found"):
            load_pdf(tmp_path / "missing.pdf")

    def test_encrypted_pdf_raises(self, tmp_path: Path) -> None:
        fake_pdf = tmp_path / "enc.pdf"
        fake_pdf.write_bytes(b"%PDF-1.4")

        with patch("fitz.open") as mock_open:
            mock_doc = MagicMock()
            mock_doc.is_encrypted = True
            mock_open.return_value = mock_doc
            with pytest.raises(IngestionError, match="password-protected"):
                load_pdf(fake_pdf)

    def test_returns_one_document_per_non_empty_page(self, tmp_path: Path) -> None:
        fake_pdf = tmp_path / "doc.pdf"
        fake_pdf.write_bytes(b"%PDF-1.4")


        with patch("fitz.open") as mock_open:
            page1 = MagicMock()
            page1.get_text.return_value = "  Page one text  "
            page2 = MagicMock()
            page2.get_text.return_value = ""  # empty page — should be skipped
            page3 = MagicMock()
            page3.get_text.return_value = "Page three text"

            mock_doc = MagicMock()
            mock_doc.is_encrypted = False
            mock_doc.__len__ = lambda self: 3
            mock_doc.load_page.side_effect = [page1, page2, page3]
            mock_doc.close = MagicMock()
            mock_open.return_value = mock_doc

            docs = load_pdf(fake_pdf)

        assert len(docs) == 2  # page 2 skipped (empty)
        assert docs[0].metadata["page"] == "1"
        assert docs[1].metadata["page"] == "3"  # page 3 after page 2 skipped
        assert docs[0].metadata["source"] == "doc.pdf"

    def test_corrupt_pdf_raises(self, tmp_path: Path) -> None:
        bad = tmp_path / "bad.pdf"
        bad.write_bytes(b"not a pdf")
        import fitz

        with patch("fitz.open", side_effect=fitz.FileDataError("corrupt")):
            with pytest.raises(IngestionError, match="Corrupt"):
                load_pdf(bad)


# ── chunk_documents ───────────────────────────────────────────────────────────

class TestChunkDocuments:
    def test_empty_input_returns_empty(self) -> None:
        assert chunk_documents([]) == []

    def test_short_text_stays_as_one_chunk(self) -> None:
        doc = _make_document("Hello world. This is a short paragraph.")
        chunks = chunk_documents([doc])
        assert len(chunks) == 1
        assert chunks[0].chunk_index == 0
        assert chunks[0].metadata["source"] == "test.pdf"

    def test_chunk_index_is_sequential_across_documents(self) -> None:
        docs = [_make_document(f"Paragraph {i}. " * 5, page=i) for i in range(1, 4)]
        chunks = chunk_documents(docs)
        indices = [c.chunk_index for c in chunks]
        assert indices == sorted(indices)
        assert indices[0] == 0

    def test_token_count_in_metadata(self) -> None:
        doc = _make_document("The quick brown fox jumps over the lazy dog.")
        chunks = chunk_documents([doc])
        assert "token_count" in chunks[0].metadata
        assert int(chunks[0].metadata["token_count"]) > 0

    def test_long_text_splits_into_multiple_chunks(self) -> None:
        # Generate ~600 tokens of text to force splitting at default 512-token limit
        long_text = "This is a test sentence with several words. " * 60
        doc = _make_document(long_text)
        chunks = chunk_documents([doc])
        assert len(chunks) > 1


# ── load_and_chunk_pdf convenience ───────────────────────────────────────────

class TestLoadAndChunkPdf:
    def test_propagates_ingestion_error(self, tmp_path: Path) -> None:
        with pytest.raises(IngestionError):
            load_and_chunk_pdf(tmp_path / "nonexistent.pdf")

    def test_returns_chunks_on_valid_pdf(self, tmp_path: Path) -> None:
        """Integration-style test using mocked fitz."""
        fake_pdf = tmp_path / "ok.pdf"
        fake_pdf.write_bytes(b"%PDF-1.4")


        with patch("fitz.open") as mock_open:
            page = MagicMock()
            page.get_text.return_value = "Business glossary definition of Customer."
            mock_doc = MagicMock()
            mock_doc.is_encrypted = False
            mock_doc.__len__ = lambda self: 1
            mock_doc.load_page.return_value = page
            mock_doc.close = MagicMock()
            mock_open.return_value = mock_doc

            chunks = load_and_chunk_pdf(fake_pdf)

        assert len(chunks) >= 1
        assert all(isinstance(c, Chunk) for c in chunks)
