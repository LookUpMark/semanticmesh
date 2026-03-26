"""Document loading (PDF and plain text) and semantic chunking.

EP-02: loads PDF pages or plain text files into Document objects, then splits
them into fixed-size Chunks using RecursiveCharacterTextSplitter. No LLM involved.
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
    """Raised when a document (PDF or text file) cannot be loaded."""


def load_pdf(path: Path) -> list[Document]:
    """Extract text from every page of a PDF file or load a plain text file.

    Args:
        path: Absolute or relative path to the PDF or text file.

    Returns:
        List of ``Document`` objects, one per page for PDFs, one document for text files.

    Raises:
        IngestionError: If the file does not exist, is encrypted, or is corrupt.
    """
    if not path.exists():
        raise IngestionError(f"File not found: {path}")

    if path.suffix.lower() in (".txt", ".md"):
        try:
            with open(path, encoding="utf-8") as f:
                text = f.read().strip()
            if not text:
                logger.debug("Empty text file: %s — skipping", path.name)
                return []
            documents = [
                Document(
                    text=text,
                    metadata={"source": path.name, "page": "1"},
                )
            ]
            logger.info("Loaded text file '%s'", path.name)
            return documents
        except Exception as exc:
            raise IngestionError(f"Failed to read text file: {path}") from exc

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


def chunk_documents_hierarchical(
    docs: list[Document],
) -> tuple[list[Chunk], list[Chunk]]:
    """Split documents into parent (512-tok) and child (128-tok) chunk hierarchies.

    Implements the Small-to-Big retrieval pattern:
    - Parents are large context nodes returned verbatim to the LLM.  They are
      NOT embedded; they are never searched directly.
    - Children are small, precisely-embedded nodes used for vector search.
      Each child carries ``parent_chunk_index`` pointing to its parent.

    Two independent splitters are created each call so that changes to
    ``settings`` (e.g. during ablation) are respected at runtime.

    Args:
        docs: List of ``Document`` objects (typically from ``load_pdf``).

    Returns:
        A ``(parents, children)`` tuple.  ``parents`` contains full-context
        chunks; ``children`` contains sub-chunks with ``parent_chunk_index`` set.
    """
    settings = get_settings()

    parent_splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.parent_chunk_size,
        chunk_overlap=settings.parent_chunk_overlap,
        # Priority: Markdown heading > paragraph > sentence > word.
        # "\n## " keeps each H2 concept section as one parent for business glossary docs.
        separators=["\n## ", "\n\n", "\n", ". ", " "],
        length_function=lambda t: len(_TOKENIZER.encode(t)),
    )
    child_splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        separators=["\n\n", "\n", ". ", " "],
        length_function=lambda t: len(_TOKENIZER.encode(t)),
    )

    parents: list[Chunk] = []
    children: list[Chunk] = []
    parent_index = 0
    child_index = 0

    for doc in docs:
        parent_splits = parent_splitter.split_text(doc.text)
        for parent_text in parent_splits:
            parent_token_count = len(_TOKENIZER.encode(parent_text))
            parents.append(
                Chunk(
                    text=parent_text,
                    chunk_index=parent_index,
                    metadata={
                        **doc.metadata,
                        "token_count": str(parent_token_count),
                    },
                )
            )

            child_splits = child_splitter.split_text(parent_text)
            for child_text in child_splits:
                child_token_count = len(_TOKENIZER.encode(child_text))
                children.append(
                    Chunk(
                        text=child_text,
                        chunk_index=child_index,
                        parent_chunk_index=parent_index,
                        metadata={
                            **doc.metadata,
                            "token_count": str(child_token_count),
                        },
                    )
                )
                child_index += 1

            parent_index += 1

    logger.info(
        "Hierarchical chunking: %d documents → %d parents (size=%d) / %d children (size=%d)",
        len(docs),
        len(parents),
        settings.parent_chunk_size,
        len(children),
        settings.chunk_size,
    )
    return parents, children
