"""Validation nodes for the Builder Graph.

This module contains the validation logic for mapping proposals, including
Pydantic schema validation, LLM critic review, and routing logic.
"""

from __future__ import annotations

import logging
from typing import Any

from src.config.llm_factory import get_midtier_llm
from src.config.logging import get_logger
from src.config.settings import get_settings
from src.mapping.validator import build_reflection_prompt, critic_review, validate_schema
from src.models.schemas import Entity, MappingProposal
from src.models.state import BuilderState

logger: logging.Logger = get_logger(__name__)


def _node_validate_mapping(state: BuilderState) -> dict[str, Any]:
    """Two-layer validation: Pydantic schema + LLM Critic."""
    settings = get_settings()
    use_lazy = bool(state.get("use_lazy_extraction", settings.use_lazy_extraction))
    llm = get_midtier_llm()
    proposal: MappingProposal | None = state.get("mapping_proposal")
    table = state.get("current_table")
    entities: list[Entity] = state.get("current_entities") or []
    attempts: int = state.get("reflection_attempts", 0)
    best_proposal: MappingProposal | None = state.get("best_proposal")

    if proposal is None:
        return {"reflection_attempts": attempts + 1}

    # Layer 1: Pydantic
    validated, error = validate_schema(proposal.model_dump())
    if error:
        if attempts >= settings.max_reflection_attempts:
            logger.warning(
                "Pydantic validation failed after %d attempts for '%s' — accepting best proposal.",
                attempts,
                proposal.table_name,
            )
            return {"reflection_attempts": 0, "hitl_flag": False}
        ref_prompt = build_reflection_prompt(
            role="data governance expert",
            output_format="JSON mapping proposal",
            error=error,
            original_input=proposal.model_dump_json(),
        )
        return {"reflection_prompt": ref_prompt, "reflection_attempts": attempts + 1}

    if best_proposal is None or (validated.confidence or 0.0) > (best_proposal.confidence or 0.0):
        best_proposal = validated

    # Optional ablation: skip critic and accept Pydantic-valid proposal directly.
    if use_lazy or not settings.enable_critic_validation:
        return {
            "mapping_proposal": validated,
            "best_proposal": None,
            "validation_error": None,
            "reflection_attempts": 0,
            "hitl_flag": validated.confidence < settings.confidence_threshold,
        }

    decision = critic_review(validated, table, entities, llm)
    if not decision.approved:
        critique = decision.critique or "Mapping rejected by critic."
        if attempts >= settings.max_reflection_attempts:
            logger.warning(
                "Critic rejected mapping for '%s' after %d attempts — accepting best proposal "
                "(concept='%s', confidence=%.2f).",
                validated.table_name,
                attempts,
                best_proposal.mapped_concept,
                best_proposal.confidence or 0.0,
            )
            return {
                "mapping_proposal": best_proposal,
                "best_proposal": None,
                "validation_error": None,
                "reflection_attempts": 0,
                "hitl_flag": False,
            }
        ref_prompt = build_reflection_prompt(
            role="data governance expert",
            output_format="JSON mapping proposal",
            error=critique,
            original_input=proposal.model_dump_json(),
        )
        return {
            "reflection_prompt": ref_prompt,
            "best_proposal": best_proposal,
            "reflection_attempts": attempts + 1,
        }

    return {
        "mapping_proposal": validated,
        "best_proposal": None,
        "validation_error": None,
        "reflection_attempts": 0,
        "hitl_flag": validated.confidence < settings.confidence_threshold,
    }


def _route_after_validate(state: BuilderState) -> str:
    if state.get("use_lazy_extraction"):
        if state.get("hitl_flag") and not state.get("skip_hitl"):
            return "hitl"
        if state.get("reflection_prompt"):
            return "rag_mapping"
        return "build_graph"

    if state.get("hitl_flag") and not state.get("skip_hitl"):
        return "hitl"
    if state.get("reflection_prompt"):
        return "rag_mapping"
    return "generate_cypher"
