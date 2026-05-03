"""Validation nodes for the Builder Graph.

This module contains the validation logic for mapping proposals, including
Pydantic schema validation, LLM critic review, and routing logic.
"""

from __future__ import annotations

import logging
from typing import Any

from src.config.llm_factory import get_midtier_llm
from src.config.logging import NodeTimer, get_logger, log_node_event
from src.config.settings import get_settings
from src.mapping.validator import build_reflection_prompt, critic_review, validate_schema
from src.models.schemas import Entity, MappingProposal
from src.models.state import BuilderState

logger: logging.Logger = get_logger(__name__)


def _node_validate_mapping(state: BuilderState) -> dict[str, Any]:
    """Two-layer validation: Pydantic schema + LLM Critic."""
    with NodeTimer() as timer:
        settings = get_settings()
        use_lazy = bool(state.get("use_lazy_extraction", settings.use_lazy_extraction))
        llm = get_midtier_llm()
        proposal: MappingProposal | None = state.get("mapping_proposal")
        table = state.get("current_table")
        entities: list[Entity] = state.get("current_entities") or []
        attempts: int = state.get("reflection_attempts", 0)
        best_proposal: MappingProposal | None = state.get("best_proposal")

        if proposal is None:
            log_node_event(logger, "validate_mapping", "no proposal", f"attempts={attempts + 1}", timer.elapsed_ms)
            return {"reflection_attempts": attempts + 1, "best_proposal": best_proposal}

        # Layer 1: Pydantic
        validated, error = validate_schema(proposal.model_dump())
        if error:
            if attempts >= settings.max_reflection_attempts:
                logger.warning(
                    "Pydantic validation failed after %d attempts for '%s' — accepting best proposal.",
                    attempts,
                    proposal.table_name,
                )
                log_node_event(logger, "validate_mapping", f"table={proposal.table_name}", "best proposal accepted", timer.elapsed_ms)
                return {
                    "mapping_proposal": best_proposal,
                    "best_proposal": None,
                    "validation_error": error,
                    "reflection_attempts": 0,
                    "hitl_flag": False,
                }
            ref_prompt = build_reflection_prompt(
                role="data governance expert",
                output_format="JSON mapping proposal",
                error=error,
                original_input=proposal.model_dump_json(),
            )
            log_node_event(logger, "validate_mapping", f"table={proposal.table_name}", f"pydantic error, retry={attempts + 1}", timer.elapsed_ms)
            return {"reflection_prompt": ref_prompt, "reflection_attempts": attempts + 1}

        if best_proposal is None or (validated.confidence or 0.0) > (best_proposal.confidence or 0.0):
            best_proposal = validated

        # Optional ablation: skip critic and accept Pydantic-valid proposal directly.
        if use_lazy or not settings.enable_critic_validation:
            log_node_event(logger, "validate_mapping", f"table={validated.table_name}", f"accepted conf={validated.confidence:.2f}", timer.elapsed_ms)
            return {
                "mapping_proposal": validated,
                "best_proposal": None,
                "validation_error": None,
                "reflection_attempts": 0,
                "hitl_flag": validated.confidence < settings.confidence_threshold,
            }

        # Confidence gate: skip expensive critic call when confidence is already high
        if (validated.confidence or 0.0) >= settings.critic_confidence_gate:
            logger.info(
                "Critic skipped for '%s': confidence %.2f >= gate %.2f.",
                validated.table_name,
                validated.confidence or 0.0,
                settings.critic_confidence_gate,
            )
            log_node_event(logger, "validate_mapping", f"table={validated.table_name}", "accepted (gate pass)", timer.elapsed_ms)
            return {
                "mapping_proposal": validated,
                "best_proposal": None,
                "validation_error": None,
                "reflection_attempts": 0,
                "hitl_flag": False,
            }

        decision = critic_review(validated, table, entities, llm)
        if not decision.approved:
            critique = decision.critique or "Mapping rejected by critic."
            if attempts >= settings.max_reflection_attempts:
                concept = best_proposal.mapped_concept if best_proposal else validated.table_name
                conf = best_proposal.confidence if best_proposal else 0.0
                logger.warning(
                    "Critic rejected mapping for '%s' after %d attempts — accepting best proposal "
                    "(concept='%s', confidence=%.2f).",
                    validated.table_name,
                    attempts,
                    concept,
                    conf,
                )
                log_node_event(logger, "validate_mapping", f"table={validated.table_name}", "best proposal accepted", timer.elapsed_ms)
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
            log_node_event(logger, "validate_mapping", f"table={validated.table_name}", f"critic rejected, retry={attempts + 1}", timer.elapsed_ms)
            return {
                "reflection_prompt": ref_prompt,
                "best_proposal": best_proposal,
                "reflection_attempts": attempts + 1,
            }

        log_node_event(logger, "validate_mapping", f"table={validated.table_name}", f"approved conf={validated.confidence:.2f}", timer.elapsed_ms)
        return {
            "mapping_proposal": validated,
            "best_proposal": None,
            "validation_error": None,
            "reflection_attempts": 0,
            "hitl_flag": validated.confidence < settings.confidence_threshold,
        }


def _route_after_validate(state: BuilderState) -> str:
    # No table currently being processed → nothing left to do
    if state.get("current_table") is None and state.get("mapping_proposal") is None:
        return "save_trace"

    # Table set but no valid proposal after exhaustion → skip to save_trace
    if state.get("mapping_proposal") is None:
        return "save_trace"

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
