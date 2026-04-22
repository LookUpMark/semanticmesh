"""Integration tests for PDF loader with LangChain OpenDataLoader.

Tests the full loading + chunking pipeline with mocked PDF extraction
but real chunking logic, verifying data flow integrity end-to-end.
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from langchain_core.documents import Document as LCDocument

from src.ingestion.pdf_loader import (
    chunk_documents,
    chunk_documents_hierarchical,
    load_pdf,
    load_pdfs_batch,
)
from src.models.schemas import Chunk, Document

pytestmark = pytest.mark.integration


def _make_lc_doc(content: str, page: int = 1, source: str = "test.pdf") -> LCDocument:
    return LCDocument(
        page_content=content,
        metadata={"source": source, "format": "markdown", "page": page},
    )


def _mock_loader(lc_docs: list[LCDocument]):
    loader = MagicMock()
    loader.load.return_value = lc_docs
    cls = MagicMock(return_value=loader)
    return cls


class TestLoadAndChunkIntegration:
    def test_pdf_to_hierarchical_chunks(self, tmp_path: Path) -> None:
        """Full flow: mock PDF load → real hierarchical chunking."""
        pdf = tmp_path / "report.pdf"
        pdf.write_bytes(b"%PDF-1.4")

        long_content = "## Introduction\n\n" + (
            "This is a detailed paragraph about customer data management. " * 40
        )
        long_content += "\n\n## Methods\n\n" + (
            "We analyzed the sales order pipeline thoroughly. " * 40
        )

        lc_docs = [
            _make_lc_doc(long_content, page=1, source="report.pdf"),
            _make_lc_doc("## Conclusion\n\nResults confirmed.", page=2, source="report.pdf"),
        ]
        mock_cls = _mock_loader(lc_docs)

        with patch("src.ingestion.pdf_loader.OpenDataLoaderPDFLoader", mock_cls):
            docs = load_pdf(pdf)

        assert len(docs) == 2

        parents, children = chunk_documents_hierarchical(docs)
        assert len(parents) >= 1
        assert len(children) >= len(parents)

        # Every child must point to a valid parent
        parent_indices = {p.chunk_index for p in parents}
        for child in children:
            assert child.parent_chunk_index in parent_indices

        # Token counts must be positive
        for chunk in parents + children:
            assert int(chunk.metadata.get("token_count", "0")) > 0

    def test_batch_loading_preserves_source_metadata(self, tmp_path: Path) -> None:
        """Batch load: each document retains its filename in metadata."""
        pdf1 = tmp_path / "alpha.pdf"
        pdf1.write_bytes(b"%PDF-1.4")
        pdf2 = tmp_path / "beta.pdf"
        pdf2.write_bytes(b"%PDF-1.4")

        lc_docs = [
            _make_lc_doc("# Alpha Doc\n\nContent A", page=1, source="alpha.pdf"),
            _make_lc_doc("# Beta Doc\n\nContent B", page=1, source="beta.pdf"),
        ]
        mock_cls = _mock_loader(lc_docs)

        with patch("src.ingestion.pdf_loader.OpenDataLoaderPDFLoader", mock_cls):
            docs = load_pdfs_batch([pdf1, pdf2])

        sources = {d.metadata["source"] for d in docs}
        assert sources == {"alpha.pdf", "beta.pdf"}

    def test_mixed_pdf_and_markdown_chunking(self, tmp_path: Path) -> None:
        """Mix of .pdf and .md files all go through the same chunking."""
        md_file = tmp_path / "glossary.md"
        md_file.write_text(
            "## Customer\n\nA person who buys products.\n\n"
            "## Product\n\nAn item available for sale.",
            encoding="utf-8",
        )
        pdf = tmp_path / "report.pdf"
        pdf.write_bytes(b"%PDF-1.4")

        lc_docs = [_make_lc_doc("# Report\n\nKey findings.", page=1, source="report.pdf")]
        mock_cls = _mock_loader(lc_docs)

        with patch("src.ingestion.pdf_loader.OpenDataLoaderPDFLoader", mock_cls):
            docs = load_pdfs_batch([md_file, pdf])

        assert len(docs) == 2
        chunks = chunk_documents(docs)
        assert len(chunks) >= 2
        assert all(isinstance(c, Chunk) for c in chunks)


class TestChunkingEdgeCases:
    def test_empty_document_list(self) -> None:
        parents, children = chunk_documents_hierarchical([])
        assert parents == []
        assert children == []

    def test_single_short_document(self) -> None:
        doc = Document(text="Short text.", metadata={"source": "s.pdf", "page": "1"})
        parents, children = chunk_documents_hierarchical([doc])
        assert len(parents) == 1
        assert len(children) >= 1
        assert children[0].parent_chunk_index == parents[0].chunk_index
