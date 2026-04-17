"""Unit tests for src/ingestion/pdf_loader.py — UT-02"""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.ingestion.pdf_loader import (
    IngestionError,
    _parse_odl_json,
    chunk_documents,
    load_and_chunk_pdf,
    load_pdf,
    load_pdfs_batch,
)
from src.models.schemas import Chunk, Document

# ── Fixtures ───────────────────────────────────────────────────────────────────


def _make_document(text: str, page: int = 1, source: str = "test.pdf") -> Document:
    return Document(text=text, metadata={"source": source, "page": str(page)})


def _make_odl_json(
    *elements: dict,
    file_name: str = "test.pdf",
) -> dict:
    """Build a minimal opendataloader JSON dict."""
    return {
        "file name": file_name,
        "number of pages": max((e.get("page number", 1) for e in elements), default=1),
        "kids": list(elements),
    }


# ── _parse_odl_json ──────────────────────────────────────────────────────────


class TestParseOdlJson:
    def test_groups_elements_by_page(self) -> None:
        elements = [
            {"type": "paragraph", "page number": 1, "content": "First page text"},
            {"type": "paragraph", "page number": 1, "content": "More on first page"},
            {"type": "paragraph", "page number": 2, "content": "Second page text"},
        ]
        doc_json = _make_odl_json(*elements)
        docs = _parse_odl_json(doc_json, "test.pdf")
        assert len(docs) == 2
        assert docs[0].metadata["page"] == "1"
        assert docs[1].metadata["page"] == "2"
        assert "First page text" in docs[0].text
        assert "More on first page" in docs[0].text

    def test_skips_empty_content(self) -> None:
        elements = [
            {"type": "paragraph", "page number": 1, "content": ""},
            {"type": "paragraph", "page number": 2, "content": "  "},
        ]
        doc_json = _make_odl_json(*elements)
        docs = _parse_odl_json(doc_json, "empty.pdf")
        assert docs == []

    def test_skips_header_and_footer(self) -> None:
        elements = [
            {"type": "header", "page number": 1, "content": "Company Confidential"},
            {"type": "paragraph", "page number": 1, "content": "Real content"},
            {"type": "footer", "page number": 1, "content": "Page 1 of 5"},
        ]
        doc_json = _make_odl_json(*elements)
        docs = _parse_odl_json(doc_json, "test.pdf")
        assert len(docs) == 1
        assert docs[0].text == "Real content"

    def test_preserves_heading_text(self) -> None:
        elements = [
            {"type": "heading", "page number": 1, "content": "Introduction", "heading level": 1},
            {"type": "paragraph", "page number": 1, "content": "Body text here."},
        ]
        doc_json = _make_odl_json(*elements)
        docs = _parse_odl_json(doc_json, "doc.pdf")
        assert len(docs) == 1
        assert "Introduction" in docs[0].text

    def test_empty_kids_returns_empty(self) -> None:
        doc_json = _make_odl_json()
        docs = _parse_odl_json(doc_json, "empty.pdf")
        assert docs == []

    def test_source_name_preserved(self) -> None:
        elements = [
            {"type": "paragraph", "page number": 1, "content": "Text"},
        ]
        doc_json = _make_odl_json(*elements)
        docs = _parse_odl_json(doc_json, "my_doc.pdf")
        assert docs[0].metadata["source"] == "my_doc.pdf"


# ── load_pdf ──────────────────────────────────────────────────────────────────


class TestLoadPdf:
    def test_file_not_found_raises(self, tmp_path: Path) -> None:
        with pytest.raises(IngestionError, match="not found"):
            load_pdf(tmp_path / "missing.pdf")

    def test_loads_text_file(self, tmp_path: Path) -> None:
        txt = tmp_path / "readme.md"
        txt.write_text("# Hello\n\nWorld", encoding="utf-8")
        docs = load_pdf(txt)
        assert len(docs) == 1
        assert docs[0].metadata["source"] == "readme.md"
        assert docs[0].metadata["page"] == "1"
        assert "Hello" in docs[0].text

    def test_skips_empty_text_file(self, tmp_path: Path) -> None:
        txt = tmp_path / "empty.txt"
        txt.write_text("   \n\n  ", encoding="utf-8")
        docs = load_pdf(txt)
        assert docs == []

    def test_pdf_uses_opendataloader(self, tmp_path: Path) -> None:
        fake_pdf = tmp_path / "doc.pdf"
        fake_pdf.write_bytes(b"%PDF-1.4")

        fake_json = _make_odl_json(
            {"type": "paragraph", "page number": 1, "content": "Page one text"},
            {"type": "paragraph", "page number": 2, "content": "Page two text"},
        )

        with (
            patch("src.ingestion.pdf_loader.opendataloader_pdf.convert") as mock_convert,
            patch("src.ingestion.pdf_loader.tempfile.TemporaryDirectory") as mock_tmpdir,
        ):
            mock_out = MagicMock()
            mock_out.__enter__ = MagicMock(return_value=str(tmp_path))
            mock_out.__exit__ = MagicMock(return_value=False)
            mock_tmpdir.return_value = mock_out

            # Write fake JSON output in the real tmp_path
            (tmp_path / "doc.json").write_text(json.dumps(fake_json), encoding="utf-8")

            docs = load_pdf(fake_pdf)

        assert len(docs) == 2
        assert docs[0].metadata["page"] == "1"
        assert docs[1].metadata["page"] == "2"
        mock_convert.assert_called_once()

    def test_pdf_error_wrapped_as_ingestion_error(self, tmp_path: Path) -> None:
        fake_pdf = tmp_path / "bad.pdf"
        fake_pdf.write_bytes(b"not a pdf")

        with (
            patch("src.ingestion.pdf_loader.opendataloader_pdf.convert") as mock_convert,
            patch("src.ingestion.pdf_loader.tempfile.TemporaryDirectory") as mock_tmpdir,
        ):
            mock_out = MagicMock()
            mock_out.__enter__ = MagicMock(return_value=str(tmp_path))
            mock_out.__exit__ = MagicMock(return_value=False)
            mock_tmpdir.return_value = mock_out

            mock_convert.side_effect = RuntimeError("corrupt PDF")
            with pytest.raises(IngestionError, match="Failed to process PDF"):
                load_pdf(fake_pdf)

    def test_pdf_no_output_raises_ingestion_error(self, tmp_path: Path) -> None:
        fake_pdf = tmp_path / "empty_output.pdf"
        fake_pdf.write_bytes(b"%PDF-1.4")

        with (
            patch("src.ingestion.pdf_loader.opendataloader_pdf.convert"),
            patch("src.ingestion.pdf_loader.tempfile.TemporaryDirectory") as mock_tmpdir,
        ):
            mock_out = MagicMock()
            mock_out.__enter__ = MagicMock(return_value=str(tmp_path))
            mock_out.__exit__ = MagicMock(return_value=False)
            mock_tmpdir.return_value = mock_out

            # Empty output dir — no JSON files
            with pytest.raises(IngestionError, match="No output from opendataloader"):
                load_pdf(fake_pdf)


# ── load_pdfs_batch ──────────────────────────────────────────────────────────


class TestLoadPdfsBatch:
    def test_file_not_found_raises(self, tmp_path: Path) -> None:
        with pytest.raises(IngestionError, match="not found"):
            load_pdfs_batch([tmp_path / "missing.pdf"])

    def test_text_files_loaded_individually(self, tmp_path: Path) -> None:
        txt1 = tmp_path / "a.md"
        txt1.write_text("Content A", encoding="utf-8")
        txt2 = tmp_path / "b.txt"
        txt2.write_text("Content B", encoding="utf-8")

        docs = load_pdfs_batch([txt1, txt2])
        assert len(docs) == 2
        assert docs[0].metadata["source"] == "a.md"
        assert docs[1].metadata["source"] == "b.txt"

    def test_mixed_pdf_and_text_files(self, tmp_path: Path) -> None:
        txt = tmp_path / "readme.md"
        txt.write_text("Text content", encoding="utf-8")
        pdf = tmp_path / "doc.pdf"
        pdf.write_bytes(b"%PDF-1.4")

        fake_json = _make_odl_json(
            {"type": "paragraph", "page number": 1, "content": "PDF content"},
        )

        with (
            patch("src.ingestion.pdf_loader.opendataloader_pdf.convert") as mock_convert,
            patch("src.ingestion.pdf_loader.tempfile.TemporaryDirectory") as mock_tmpdir,
        ):
            mock_out = MagicMock()
            mock_out.__enter__ = MagicMock(return_value=str(tmp_path))
            mock_out.__exit__ = MagicMock(return_value=False)
            mock_tmpdir.return_value = mock_out

            # Write fake JSON output
            (tmp_path / "doc.json").write_text(json.dumps(fake_json), encoding="utf-8")

            docs = load_pdfs_batch([txt, pdf])

        assert len(docs) == 2
        assert docs[0].metadata["source"] == "readme.md"
        assert docs[1].metadata["source"] == "doc.pdf"
        mock_convert.assert_called_once()

    def test_batch_passes_all_pdfs_to_convert(self, tmp_path: Path) -> None:
        pdf1 = tmp_path / "a.pdf"
        pdf1.write_bytes(b"%PDF-1.4")
        pdf2 = tmp_path / "b.pdf"
        pdf2.write_bytes(b"%PDF-1.4")

        fake_json_a = _make_odl_json(
            {"type": "paragraph", "page number": 1, "content": "A content"},
            file_name="a.pdf",
        )
        fake_json_b = _make_odl_json(
            {"type": "paragraph", "page number": 1, "content": "B content"},
            file_name="b.pdf",
        )

        with (
            patch("src.ingestion.pdf_loader.opendataloader_pdf.convert") as mock_convert,
            patch("src.ingestion.pdf_loader.tempfile.TemporaryDirectory") as mock_tmpdir,
        ):
            mock_out = MagicMock()
            mock_out.__enter__ = MagicMock(return_value=str(tmp_path))
            mock_out.__exit__ = MagicMock(return_value=False)
            mock_tmpdir.return_value = mock_out

            (tmp_path / "a.json").write_text(json.dumps(fake_json_a), encoding="utf-8")
            (tmp_path / "b.json").write_text(json.dumps(fake_json_b), encoding="utf-8")

            docs = load_pdfs_batch([pdf1, pdf2])

        # Verify convert was called with both PDFs in one batch
        call_args = mock_convert.call_args
        input_paths = (
            call_args.kwargs.get("input_path") or call_args[1].get("input_path") or call_args[0][0]
        )
        assert len(input_paths) == 2
        assert len(docs) == 2


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
        # Generate ~600 tokens of text to force splitting at default 256-token limit
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
        """Integration-style test using mocked opendataloader."""
        fake_pdf = tmp_path / "ok.pdf"
        fake_pdf.write_bytes(b"%PDF-1.4")

        fake_json = _make_odl_json(
            {
                "type": "paragraph",
                "page number": 1,
                "content": "Business glossary definition of Customer.",
            },
        )

        with (
            patch("src.ingestion.pdf_loader.opendataloader_pdf.convert"),
            patch("src.ingestion.pdf_loader.tempfile.TemporaryDirectory") as mock_tmpdir,
        ):
            mock_out = MagicMock()
            mock_out.__enter__ = MagicMock(return_value=str(tmp_path))
            mock_out.__exit__ = MagicMock(return_value=False)
            mock_tmpdir.return_value = mock_out

            (tmp_path / "ok.json").write_text(json.dumps(fake_json), encoding="utf-8")

            chunks = load_and_chunk_pdf(fake_pdf)

        assert len(chunks) >= 1
        assert all(isinstance(c, Chunk) for c in chunks)
