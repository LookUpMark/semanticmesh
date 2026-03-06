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
                metadata={"source": path.name, "page": str(page_index + 1)},
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
                        "token_count": str(token_count),
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
