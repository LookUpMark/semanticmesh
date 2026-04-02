"""Shared JSON parsing and reflection utilities for LLM outputs.

This module provides common patterns used across the codebase for handling
LLM-generated JSON responses, including markdown fence stripping and self-
reflection retry loops for handling parse/validation errors.
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from src.config.llm_client import LLMProtocol

# Matches optional triple-backtick markdown fences (with or without language tag)
_FENCE_RE = re.compile(r"^```[a-zA-Z]*\n?|```$", re.MULTILINE)


def extract_text_content(content: str | list) -> str:
    """Extract plain text from an LLM response content field.

    OpenRouter models with reasoning tokens (e.g. gpt-oss-120b, gpt-5-nano)
    return ``response.content`` as a list of content blocks instead of a plain
    string.  This helper normalises both forms to a single string.

    Args:
        content: Either a plain ``str`` or a list of content blocks
                 (dicts with ``{"type": "text", "text": "..."}`` or objects
                 with ``.type`` / ``.text`` attributes).

    Returns:
        Concatenated text content, or ``""`` if no text blocks are found.
    """
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for block in content:
            if isinstance(block, dict):
                if block.get("type") == "text":
                    parts.append(block.get("text", ""))
            elif hasattr(block, "type") and block.type == "text":
                parts.append(getattr(block, "text", ""))
        return "\n".join(parts)
    return str(content)


def clean_json(raw: str) -> str:
    """Strip markdown fences and extract JSON from LLM output.

    Many LLMs wrap JSON in ```json ... ``` or ``` ... ``` despite instructions
    to output raw JSON. This function strips those fences and extracts the
    JSON object from within larger text blocks.

    Handles:
    - Markdown fences (```json ... ```)
    - Extra text before/after the JSON object
    - Leading/trailing whitespace

    Args:
        raw: Raw LLM response content that may contain markdown fences or extra text.

    Returns:
        Cleaned JSON string with fences removed and JSON object extracted.

    Example:
        >>> clean_json('```json\\n{"key": "value"}\\n```')
        '{"key": "value"}'
        >>> clean_json('Here is the result: {"key": "value"} - done')
        '{"key": "value"}'
        >>> clean_json('  {"key": "value"}  ')
        '{"key": "value"}'
    """
    cleaned = _FENCE_RE.sub("", raw).strip()
    # Extract JSON object from within larger text
    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start != -1 and end != -1 and end > start:
        return cleaned[start : end + 1]
    return cleaned


class ReflectionResult(TypedDict):
    """Result of a reflection retry attempt.

    Attributes:
        success: Whether the reflection produced a valid JSON string.
        content: The reflected JSON content (may be empty on failure).
        error: Error message if reflection failed, None otherwise.
    """

    success: bool
    content: str
    error: str | None


def reflect_on_json(
    llm: LLMProtocol,
    error: str,
    original_input: str,
    role: str,
    output_format: str,
    max_attempts: int = 1,
    truncated: bool = False,
) -> ReflectionResult:
    """Ask the LLM to self-correct a malformed JSON output.

    Uses a reflection prompt template to inject the original raw response
    and the parse/validation error, requesting a corrected JSON string.

    When ``truncated=True`` (the original response was empty because the model
    hit the max_tokens cap), the prompt instructs the model to re-extract with
    a strict limit so the output fits within the token budget.

    Args:
        llm: LLM instance to invoke for reflection.
        error: The ``json.JSONDecodeError`` or ``ValidationError`` message.
        original_input: The original (broken) LLM output string.
        role: Description of the LLM's role (e.g., "strict information extraction
            engine").
        output_format: Expected output format description (e.g., 'JSON object matching
            {"key": ...}').
        max_attempts: Maximum reflection retry attempts (default: 1).
        truncated: Set to True when original_input is empty (cap hit on first call).

    Returns:
        ``ReflectionResult`` with success status and corrected content.

    Example:
        >>> result = reflect_on_json(
        ...     llm,
        ...     error="Expecting property name enclosed in double quotes",
        ...     original_input='{"key": invalid}',
        ...     role="strict information extraction engine",
        ...     output_format='JSON object matching {"triplets": [...]}'
        ... )
        >>> if result["success"]:
        ...     data = json.loads(result["content"])
    """
    if truncated:
        # The response was empty because the model hit the output token cap.
        # Ask for a concise re-extraction with a hard limit.
        prompt = (
            "Your previous response was cut off because it exceeded the output token limit.\n"
            "Re-extract from the original text, but limit yourself to the "
            "10 most important facts. "
            f"Output ONLY valid {output_format}. No explanation, no markdown."
        )
    else:
        from src.prompts.templates import REFLECTION_TEMPLATE

        prompt = REFLECTION_TEMPLATE.format(
            role=role,
            output_format=output_format,
            error_or_critique=error,
            original_input=original_input,
        )

    try:
        response = llm.invoke([{"role": "user", "content": prompt}])
        content = extract_text_content(response.content)
        cleaned = clean_json(content) if content else ""
        return ReflectionResult(success=True, content=cleaned, error=None)
    except Exception as exc:
        return ReflectionResult(success=False, content="", error=str(exc))
