"""Document loading (PDF and plain text) and semantic chunking.

EP-02: loads PDF pages or plain text files into Document objects, then splits
them into fixed-size Chunks using RecursiveCharacterTextSplitter. No LLM involved.

PDF extraction uses the official LangChain integration for opendataloader-pdf
(``langchain-opendataloader-pdf``). Markdown output is requested so that heading
hierarchy, tables, and lists are preserved verbatim — this is especially valuable
for the parent splitter in ``chunk_documents_hierarchical`` which already splits
on ``"\n## "`` boundaries.
"""

from __future__ import annotations

import logging
from pathlib import Path

import tiktoken
from langchain_opendataloader_pdf import OpenDataLoaderPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.config.logging import get_logger
from src.config.settings import get_settings
from src.models.schemas import Chunk, Document

logger: logging.Logger = get_logger(__name__)

_settings = get_settings()
_TOKENIZER = tiktoken.get_encoding("cl100k_base")


class IngestionError(Exception):
    """Raised when a document (PDF or text file) cannot be loaded."""


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _load_text_file(path: Path) -> list[Document]:
    """Load a .txt or .md file into a single Document."""
    try:
        with open(path, encoding="utf-8") as f:
            text = f.read().strip()
        if not text:
            logger.debug("Empty text file: %s — skipping", path.name)
            return []
        logger.info("Loaded text file '%s'", path.name)
        return [
            Document(text=text, metadata={"source": path.name, "page": "1"}),
        ]
    except Exception as exc:
        raise IngestionError(f"Failed to read text file: {path}") from exc


def _lc_docs_to_documents(
    lc_docs: list,
    source_name: str,
) -> list[Document]:
    """Convert LangChain Document objects returned by OpenDataLoaderPDFLoader
    into our internal ``Document`` schema.

    Each LangChain document has ``page_content`` (Markdown text) and
    ``metadata["page"]`` (1-indexed page number).  Headers/footers are already
    excluded by the loader (``include_header_footer=False`` default).
    """
    documents: list[Document] = []
    for lc_doc in lc_docs:
        content = lc_doc.page_content.strip()
        if not content:
            continue
        page = lc_doc.metadata.get("page", 1)
        documents.append(
            Document(
                text=content,
                metadata={"source": source_name, "page": str(page)},
            )
        )
    return documents


def _load_pdf_via_opendataloader(path: Path) -> list[Document]:
    """Extract text from a PDF using the LangChain OpenDataLoader integration.

    Uses ``OpenDataLoaderPDFLoader`` with Markdown output so that heading
    hierarchy, table structure, and list formatting are preserved.
    Headers and footers are excluded by the loader (default behaviour).
    """
    loader = OpenDataLoaderPDFLoader(
        file_path=str(path),
        format="markdown",
        split_pages=True,
        include_header_footer=False,
        quiet=True,
    )
    lc_docs = loader.load()
    documents = _lc_docs_to_documents(lc_docs, path.name)

    if not documents:
        logger.debug("All pages empty in %s — skipping", path.name)
        return []

    logger.info("Loaded %d pages from '%s'", len(documents), path.name)
    return documents


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def load_pdf(path: Path) -> list[Document]:
    """Extract text from every page of a PDF file or load a plain text file.

    Args:
        path: Absolute or relative path to the PDF or text file.

    Returns:
        List of ``Document`` objects, one per page for PDFs, one document for text files.

    Raises:
        IngestionError: If the file does not exist or cannot be processed.
    """
    if not path.exists():
        raise IngestionError(f"File not found: {path}")

    if path.suffix.lower() in (".txt", ".md"):
        return _load_text_file(path)

    try:
        return _load_pdf_via_opendataloader(path)
    except IngestionError:
        raise
    except Exception as exc:
        raise IngestionError(f"Failed to process PDF: {path}") from exc


def load_pdfs_batch(paths: list[Path]) -> list[Document]:
    """Load multiple files in a single opendataloader-pdf call.

    Batches all PDFs into one ``convert()`` call to amortise JVM startup cost.
    Plain text files (.txt, .md) are loaded individually outside the batch.

    Args:
        paths: List of file paths (PDFs, .txt, or .md files).

    Returns:
        Concatenated list of ``Document`` objects from all files.

    Raises:
        IngestionError: If any file is not found or cannot be processed.
    """
    pdf_paths: list[Path] = []
    text_paths: list[Path] = []
    for p in paths:
        if not p.exists():
            raise IngestionError(f"File not found: {p}")
        if p.suffix.lower() in (".txt", ".md"):
            text_paths.append(p)
        else:
            pdf_paths.append(p)

    all_docs: list[Document] = []

    # Load text files individually (no JVM needed).
    for tp in text_paths:
        all_docs.extend(_load_text_file(tp))

    # Batch all PDFs into one loader call (single JVM invocation).
    if pdf_paths:
        loader = OpenDataLoaderPDFLoader(
            file_path=[str(p) for p in pdf_paths],
            format="markdown",
            split_pages=True,
            include_header_footer=False,
            quiet=True,
        )
        lc_docs = loader.load()

        # Group by source filename so we can log per-file counts.
        from collections import defaultdict

        per_file: dict[str, list] = defaultdict(list)
        for lc_doc in lc_docs:
            src = Path(lc_doc.metadata.get("source", "")).name
            per_file[src].append(lc_doc)

        for pdf_path in pdf_paths:
            file_lc_docs = per_file.get(pdf_path.name, [])
            if not file_lc_docs:
                logger.warning("No output for '%s' — skipping", pdf_path.name)
                continue
            docs = _lc_docs_to_documents(file_lc_docs, pdf_path.name)
            if docs:
                logger.info("Loaded %d pages from '%s'", len(docs), pdf_path.name)
                all_docs.extend(docs)
            else:
                logger.debug("All pages empty in %s — skipping", pdf_path.name)

    return all_docs


# ---------------------------------------------------------------------------
# Chunking (unchanged — operates on Document objects regardless of source)
# ---------------------------------------------------------------------------


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
