"""Unit tests for src/ingestion/pdf_loader.py — UT-02"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from langchain_core.documents import Document as LCDocument

from src.ingestion.pdf_loader import (
    IngestionError,
    _lc_docs_to_documents,
    chunk_documents,
    load_and_chunk_pdf,
    load_pdf,
    load_pdfs_batch,
)
from src.models.schemas import Chunk, Document

# ── Fixtures ───────────────────────────────────────────────────────────────────


def _make_document(text: str, page: int = 1, source: str = "test.pdf") -> Document:
    return Document(text=text, metadata={"source": source, "page": str(page)})


def _make_lc_doc(content: str, page: int = 1, source: str = "test.pdf") -> LCDocument:
    """Build a minimal LangChain Document as returned by OpenDataLoaderPDFLoader."""
    return LCDocument(
        page_content=content,
        metadata={"source": source, "format": "markdown", "page": page},
    )


def _make_loader_mock(lc_docs: list[LCDocument]) -> MagicMock:
    """Return a mock that behaves like OpenDataLoaderPDFLoader(...)."""
    loader_instance = MagicMock()
    loader_instance.load.return_value = lc_docs
    mock_cls = MagicMock(return_value=loader_instance)
    return mock_cls


# ── _lc_docs_to_documents ─────────────────────────────────────────────────────


class TestLcDocsToDocuments:
    def test_maps_page_content_and_metadata(self) -> None:
        lc_docs = [
            _make_lc_doc("# Intro\n\nFirst page text", page=1),
            _make_lc_doc("Second page text", page=2),
        ]
        docs = _lc_docs_to_documents(lc_docs, "test.pdf")
        assert len(docs) == 2
        assert docs[0].metadata["page"] == "1"
        assert docs[1].metadata["page"] == "2"
        assert "# Intro" in docs[0].text
        assert "First page text" in docs[0].text

    def test_skips_empty_page_content(self) -> None:
        lc_docs = [
            _make_lc_doc("", page=1),
            _make_lc_doc("   ", page=2),
        ]
        docs = _lc_docs_to_documents(lc_docs, "empty.pdf")
        assert docs == []

    def test_source_name_overrides_metadata(self) -> None:
        lc_docs = [_make_lc_doc("Text", page=1, source="/some/path/original.pdf")]
        docs = _lc_docs_to_documents(lc_docs, "my_doc.pdf")
        assert docs[0].metadata["source"] == "my_doc.pdf"

    def test_preserves_markdown_structure(self) -> None:
        markdown_content = "# Heading\n\n## Subheading\n\n| Col1 | Col2 |\n|------|------|\n| A    | B    |"
        lc_docs = [_make_lc_doc(markdown_content, page=1)]
        docs = _lc_docs_to_documents(lc_docs, "table.pdf")
        assert "# Heading" in docs[0].text
        assert "## Subheading" in docs[0].text
        assert "| Col1 |" in docs[0].text

    def test_page_defaults_to_one_when_missing(self) -> None:
        lc_doc = LCDocument(page_content="Content", metadata={"source": "doc.pdf", "format": "markdown"})
        docs = _lc_docs_to_documents([lc_doc], "doc.pdf")
        assert docs[0].metadata["page"] == "1"


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

    def test_pdf_uses_langchain_loader(self, tmp_path: Path) -> None:
        fake_pdf = tmp_path / "doc.pdf"
        fake_pdf.write_bytes(b"%PDF-1.4")

        lc_docs = [
            _make_lc_doc("# Page one\n\nPage one text", page=1, source="doc.pdf"),
            _make_lc_doc("Page two text", page=2, source="doc.pdf"),
        ]
        mock_cls = _make_loader_mock(lc_docs)

        with patch("src.ingestion.pdf_loader.OpenDataLoaderPDFLoader", mock_cls):
            docs = load_pdf(fake_pdf)

        assert len(docs) == 2
        assert docs[0].metadata["page"] == "1"
        assert docs[1].metadata["page"] == "2"
        mock_cls.assert_called_once_with(
            file_path=str(fake_pdf),
            format="markdown",
            split_pages=True,
            include_header_footer=False,
            quiet=True,
        )

    def test_pdf_error_wrapped_as_ingestion_error(self, tmp_path: Path) -> None:
        fake_pdf = tmp_path / "bad.pdf"
        fake_pdf.write_bytes(b"not a pdf")

        mock_cls = MagicMock()
        mock_cls.return_value.load.side_effect = RuntimeError("corrupt PDF")

        with patch("src.ingestion.pdf_loader.OpenDataLoaderPDFLoader", mock_cls):
            with pytest.raises(IngestionError, match="Failed to process PDF"):
                load_pdf(fake_pdf)

    def test_pdf_all_empty_pages_returns_empty(self, tmp_path: Path) -> None:
        fake_pdf = tmp_path / "blank.pdf"
        fake_pdf.write_bytes(b"%PDF-1.4")

        lc_docs = [
            _make_lc_doc("", page=1, source="blank.pdf"),
            _make_lc_doc("   ", page=2, source="blank.pdf"),
        ]
        mock_cls = _make_loader_mock(lc_docs)

        with patch("src.ingestion.pdf_loader.OpenDataLoaderPDFLoader", mock_cls):
            docs = load_pdf(fake_pdf)

        assert docs == []


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

        lc_docs = [_make_lc_doc("# PDF Heading\n\nPDF content", page=1, source="doc.pdf")]
        mock_cls = _make_loader_mock(lc_docs)

        with patch("src.ingestion.pdf_loader.OpenDataLoaderPDFLoader", mock_cls):
            docs = load_pdfs_batch([txt, pdf])

        assert len(docs) == 2
        assert docs[0].metadata["source"] == "readme.md"
        assert docs[1].metadata["source"] == "doc.pdf"
        mock_cls.assert_called_once()

    def test_batch_passes_all_pdfs_to_loader(self, tmp_path: Path) -> None:
        pdf1 = tmp_path / "a.pdf"
        pdf1.write_bytes(b"%PDF-1.4")
        pdf2 = tmp_path / "b.pdf"
        pdf2.write_bytes(b"%PDF-1.4")

        lc_docs = [
            _make_lc_doc("A content", page=1, source="a.pdf"),
            _make_lc_doc("B content", page=1, source="b.pdf"),
        ]
        mock_cls = _make_loader_mock(lc_docs)

        with patch("src.ingestion.pdf_loader.OpenDataLoaderPDFLoader", mock_cls):
            docs = load_pdfs_batch([pdf1, pdf2])

        # Loader instantiated once with both paths
        call_kwargs = mock_cls.call_args.kwargs
        assert set(call_kwargs["file_path"]) == {str(pdf1), str(pdf2)}
        assert call_kwargs["format"] == "markdown"
        assert len(docs) == 2

    def test_missing_pdf_in_loader_output_skips_gracefully(self, tmp_path: Path) -> None:
        pdf1 = tmp_path / "found.pdf"
        pdf1.write_bytes(b"%PDF-1.4")
        pdf2 = tmp_path / "empty.pdf"
        pdf2.write_bytes(b"%PDF-1.4")

        # Loader only returns docs for found.pdf — empty.pdf produces nothing
        lc_docs = [_make_lc_doc("Found content", page=1, source="found.pdf")]
        mock_cls = _make_loader_mock(lc_docs)

        with patch("src.ingestion.pdf_loader.OpenDataLoaderPDFLoader", mock_cls):
            docs = load_pdfs_batch([pdf1, pdf2])

        assert len(docs) == 1
        assert docs[0].metadata["source"] == "found.pdf"


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
        """Integration-style test using mocked OpenDataLoaderPDFLoader."""
        fake_pdf = tmp_path / "ok.pdf"
        fake_pdf.write_bytes(b"%PDF-1.4")

        lc_docs = [
            _make_lc_doc(
                "## Customer\n\nBusiness glossary definition of Customer.",
                page=1,
                source="ok.pdf",
            )
        ]
        mock_cls = _make_loader_mock(lc_docs)

        with patch("src.ingestion.pdf_loader.OpenDataLoaderPDFLoader", mock_cls):
            chunks = load_and_chunk_pdf(fake_pdf)

        assert len(chunks) >= 1
        assert all(isinstance(c, Chunk) for c in chunks)
