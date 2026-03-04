# Part 3 — `src/ingestion/pdf_loader.py`

## 1. Purpose & Context

**Epic:** EP-02 PDF ingestion  
**US-02-01** — PDF Loading, **US-02-02** — Semantic Chunking

Handles the first two steps of the pipeline: raw PDF extraction and text chunking into bounded segments ready for SLM processing. No LLM is involved — this is pure deterministic ETL.

---

## 2. Prerequisites

- `src/models/schemas.py` — `Document`, `Chunk` (step 3)
- `src/config/settings.py` — `chunk_size`, `chunk_overlap` (step 2)
- `src/config/logging.py` — `get_logger` (step 3 infra)
- Dependencies: `pymupdf>=1.24`, `langchain-text-splitters>=0.3`, `tiktoken>=0.7`

---

## 3. Public API

| Symbol | Signature | Description |
|---|---|---|
| `IngestionError` | `class(Exception)` | Raised on corrupt / password-protected PDFs |
| `load_pdf` | `(path: Path) -> list[Document]` | Extracts raw text, one `Document` per page |
| `chunk_documents` | `(docs: list[Document]) -> list[Chunk]` | Splits into ≤`chunk_size`-token chunks |
| `load_and_chunk_pdf` | `(path: Path) -> list[Chunk]` | Convenience: `load_pdf` + `chunk_documents` |

---

## 4. Full Implementation

```python
"""PDF loading and semantic chunking.

EP-02: loads PDF pages into Document objects, then splits them into
fixed-size Chunks using RecursiveCharacterTextSplitter.  No LLM involved.
"""

from __future__ import annotations

import logging
from pathlib import Path

import fitz  # pymupdf
import tiktoken
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.config.logging import get_logger
from src.config.settings import get_settings
from src.models.schemas import Chunk, Document

logger: logging.Logger = get_logger(__name__)

_settings = get_settings()
_TOKENIZER = tiktoken.get_encoding("cl100k_base")


class IngestionError(Exception):
    """Raised when a PDF cannot be loaded (corrupt, encrypted, missing)."""


def load_pdf(path: Path) -> list[Document]:
    """Extract text from every page of a PDF file.

    Args:
        path: Absolute or relative path to the PDF file.

    Returns:
        List of ``Document`` objects, one per page, preserving page number.

    Raises:
        IngestionError: If the file does not exist, is encrypted, or is corrupt.
    """
    if not path.exists():
        raise IngestionError(f"PDF file not found: {path}")

    try:
        pdf = fitz.open(str(path))
    except fitz.FileDataError as exc:
        raise IngestionError(f"Corrupt or unsupported PDF: {path}") from exc

    if pdf.is_encrypted:
        raise IngestionError(f"PDF is password-protected: {path}")

    documents: list[Document] = []
    for page_index in range(len(pdf)):
        page = pdf.load_page(page_index)
        text = page.get_text("text").strip()
        if not text:
            logger.debug("Empty page %d in %s — skipping", page_index + 1, path.name)
            continue
        documents.append(
            Document(
                text=text,
                metadata={"source": path.name, "page": page_index + 1},
            )
        )

    pdf.close()
    logger.info("Loaded %d pages from '%s'", len(documents), path.name)
    return documents


def chunk_documents(docs: list[Document]) -> list[Chunk]:
    """Split documents into fixed-size chunks with overlap.

    Uses ``RecursiveCharacterTextSplitter`` with separators that respect
    paragraph, sentence, and word boundaries in that priority order.
    Token count is estimated via ``tiktoken`` (cl100k_base).

    Args:
        docs: List of ``Document`` objects (typically from ``load_pdf``).

    Returns:
        List of ``Chunk`` objects preserving source / page metadata.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=_settings.chunk_size,
        chunk_overlap=_settings.chunk_overlap,
        separators=["\n\n", "\n", ". ", " "],
        length_function=lambda t: len(_TOKENIZER.encode(t)),
    )

    chunks: list[Chunk] = []
    chunk_index = 0

    for doc in docs:
        splits = splitter.split_text(doc.text)
        for split_text in splits:
            token_count = len(_TOKENIZER.encode(split_text))
            chunks.append(
                Chunk(
                    text=split_text,
                    chunk_index=chunk_index,
                    metadata={
                        **doc.metadata,
                        "token_count": token_count,
                    },
                )
            )
            chunk_index += 1

    logger.info(
        "Chunked %d documents into %d chunks (chunk_size=%d, overlap=%d)",
        len(docs),
        len(chunks),
        _settings.chunk_size,
        _settings.chunk_overlap,
    )
    return chunks


def load_and_chunk_pdf(path: Path) -> list[Chunk]:
    """Convenience function: load a PDF and immediately chunk it.

    Args:
        path: Path to the PDF file.

    Returns:
        List of text chunks ready for SLM processing.

    Raises:
        IngestionError: propagated from ``load_pdf``.
    """
    docs = load_pdf(path)
    return chunk_documents(docs)
```

---

## 5. Tests

```python
"""Unit tests for src/ingestion/pdf_loader.py — UT-02"""

from __future__ import annotations

import io
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.ingestion.pdf_loader import (
    IngestionError,
    chunk_documents,
    load_and_chunk_pdf,
    load_pdf,
)
from src.models.schemas import Chunk, Document


# ── Fixtures ───────────────────────────────────────────────────────────────────

def _make_document(text: str, page: int = 1, source: str = "test.pdf") -> Document:
    return Document(text=text, metadata={"source": source, "page": page})


# ── load_pdf ──────────────────────────────────────────────────────────────────

class TestLoadPdf:
    def test_file_not_found_raises(self, tmp_path: Path) -> None:
        with pytest.raises(IngestionError, match="not found"):
            load_pdf(tmp_path / "missing.pdf")

    def test_encrypted_pdf_raises(self, tmp_path: Path) -> None:
        fake_pdf = tmp_path / "enc.pdf"
        fake_pdf.write_bytes(b"%PDF-1.4")
        import fitz
        with patch("fitz.open") as mock_open:
            mock_doc = MagicMock()
            mock_doc.is_encrypted = True
            mock_open.return_value = mock_doc
            with pytest.raises(IngestionError, match="password-protected"):
                load_pdf(fake_pdf)

    def test_returns_one_document_per_non_empty_page(self, tmp_path: Path) -> None:
        fake_pdf = tmp_path / "doc.pdf"
        fake_pdf.write_bytes(b"%PDF-1.4")

        import fitz
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
        assert docs[0].metadata["page"] == 1
        assert docs[1].metadata["page"] == 3
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
        assert chunks[0].metadata["token_count"] > 0

    def test_long_text_splits_into_multiple_chunks(self) -> None:
        # Generate ~600 tokens of text to force splitting at default 512-token limit
        long_text = ("This is a test sentence with several words. " * 60)
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

        import fitz
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
```

---

## 6. Smoke Test

```bash
# Requires a real PDF in tests/fixtures/sample_docs/
python -c "
from pathlib import Path
from src.ingestion.pdf_loader import load_and_chunk_pdf
chunks = load_and_chunk_pdf(Path('tests/fixtures/sample_docs/sample_glossary.pdf'))
print(f'Loaded {len(chunks)} chunks')
print(f'First chunk: {chunks[0].text[:120]!r}')
"
```
