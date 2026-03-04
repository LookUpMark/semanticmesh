# Part 5 — `src/mapping/hitl.py`

## 1. Purpose & Context

**Epic:** EP-08 Human-in-the-Loop Breakpoint  
**US-08-01** — LangGraph `interrupt()` integration

The HITL node is a conditional breakpoint in the Builder Graph. When triggered it:

1. **Suspends** execution by calling `langgraph.types.interrupt()`.
2. **Delivers** a structured payload to the human reviewer via the checkpoint store.
3. **Waits** for a `Command` resumption carrying one of three actions: `"approve"`, `"correct"`, or `"reject"`.
4. **Patches** the state and routes to the next node (`Generate_Cypher`, `Skip`, or raises `ValueError`).

Checkpointing uses `MemorySaver` (development) or `SqliteSaver` (production) passed in at graph-compile time.

---

## 2. Prerequisites

- `src/models/schemas.py` — `MappingProposal`, `Entity` (step 5)
- `src/models/state.py` — `BuilderState` with `hitl_flag`, `current_table`, `mapping_proposal`, `current_entities` (step 6)
- LangGraph ≥ 0.2.35 — `interrupt()` from `langgraph.types`, `Command` from `langgraph.types`
- `src/config/logging.py` — `get_logger`

---

## 3. Public API

| Symbol | Signature | Description |
|---|---|---|
| `hitl_node` | `(state: BuilderState) -> Command` | LangGraph node; interrupts if `hitl_flag=True` or confidence < 0.9 |
| `should_interrupt` | `(state: BuilderState) -> bool` | Pure predicate; usable as conditional edge |
| `build_interrupt_payload` | `(proposal: MappingProposal, entities: list[Entity]) -> dict` | Assembles the structured dict given to the human reviewer |

---

## 4. Full Implementation

```python
"""Human-in-the-Loop breakpoint node for the Builder Graph.

EP-08 / US-08-01: Calls langgraph.types.interrupt() to suspend the graph
and wait for human input (approve / correct / reject).
"""

from __future__ import annotations

import logging
from typing import Literal

from langgraph.types import Command, interrupt

from src.config.logging import get_logger
from src.models.schemas import Entity, MappingProposal
from src.models.state import BuilderState

logger: logging.Logger = get_logger(__name__)

# Threshold below which the HITL breakpoint is automatically triggered.
_CONFIDENCE_THRESHOLD: float = 0.9

HumanAction = Literal["approve", "correct", "reject"]


# ── Pure Predicate ─────────────────────────────────────────────────────────────

def should_interrupt(state: BuilderState) -> bool:
    """Return True if the HITL breakpoint must fire.

    Triggers when:
    - the graph's ``hitl_flag`` is explicitly set to True, OR
    - the current mapping proposal has confidence below ``_CONFIDENCE_THRESHOLD``.

    This function is used both inside ``hitl_node`` and as a conditional edge
    predicate so the graph can skip the node entirely on high-confidence runs.
    """
    if state.get("hitl_flag", False):
        return True
    proposal: MappingProposal | None = state.get("mapping_proposal")
    if proposal is not None and proposal.confidence < _CONFIDENCE_THRESHOLD:
        return True
    return False


# ── Payload Builder ────────────────────────────────────────────────────────────

def build_interrupt_payload(
    proposal: MappingProposal,
    entities: list[Entity],
) -> dict:
    """Assemble the structured payload delivered to the human reviewer.

    Args:
        proposal: The candidate mapping from ``propose_mapping``.
        entities: All resolved entities available; used to list alternatives.

    Returns:
        A plain ``dict`` that the checkpoint store serialises for the reviewer.
        Keys:
        - ``table_name`` — table being mapped
        - ``proposed_concept`` — chosen business concept
        - ``confidence`` — [0.0, 1.0] score
        - ``reasoning`` — LLM rationale
        - ``alternative_concepts`` — up to 4 other candidates
        - ``provenance_text`` — concatenated provenance texts from top entities
    """
    all_concept_names: list[str] = [e.name for e in entities if e.name != proposal.mapped_concept]
    alternatives: list[str] = (proposal.alternative_concepts or []) + all_concept_names
    unique_alternatives: list[str] = list(dict.fromkeys(alternatives))[:4]

    provenance_texts: list[str] = [
        e.provenance_text for e in entities[:3] if e.provenance_text
    ]

    return {
        "table_name": proposal.table_name,
        "proposed_concept": proposal.mapped_concept,
        "confidence": proposal.confidence,
        "reasoning": proposal.reasoning,
        "alternative_concepts": unique_alternatives,
        "provenance_text": " | ".join(provenance_texts),
    }


# ── HITL LangGraph Node ────────────────────────────────────────────────────────

def hitl_node(state: BuilderState) -> Command:
    """LangGraph node that suspends execution pending human review.

    If ``should_interrupt`` is False the node skips the interrupt and returns a
    ``Command(goto="Generate_Cypher")`` immediately (pass-through).

    When interrupted, the graph resumes only after a human sends a ``Command``
    resumption value with structure::

        {
            "action": "approve" | "correct" | "reject",
            "mapped_concept": "<str>"   # only required for "correct"
        }

    On ``"approve"`` — routes to ``"Generate_Cypher"`` unchanged.
    On ``"correct"`` — patches ``mapping_proposal.mapped_concept`` and routes to ``"Generate_Cypher"``.
    On ``"reject"``  — marks ``rejected=True`` and routes to ``"End"``.

    Args:
        state: Current ``BuilderState`` snapshot.

    Returns:
        A LangGraph ``Command`` that updates state and selects the next node.
    """
    proposal: MappingProposal | None = state.get("mapping_proposal")
    entities: list[Entity] = state.get("current_entities") or []

    # ── Pass-through if no interrupt needed ──
    if not should_interrupt(state):
        logger.debug(
            "HITL pass-through: confidence=%.2f ≥ %.2f",
            proposal.confidence if proposal else 0.0,
            _CONFIDENCE_THRESHOLD,
        )
        return Command(goto="Generate_Cypher")

    if proposal is None:
        logger.warning("HITL triggered but mapping_proposal is None — routing to End.")
        return Command(update={"rejected": True}, goto="End")

    payload = build_interrupt_payload(proposal, entities)
    logger.info(
        "HITL interrupt fired for table '%s' (confidence=%.2f).",
        proposal.table_name, proposal.confidence,
    )

    # ── Suspend and wait for human input ──────────────────────────────────────
    human_response: dict = interrupt(payload)
    # Execution resumes only after a Command is submitted by the human.
    # ``human_response`` is whatever dict the reviewer provides.

    action: HumanAction = human_response.get("action", "approve")

    if action == "approve":
        logger.info("HITL: human approved mapping '%s'.", proposal.mapped_concept)
        return Command(goto="Generate_Cypher")

    if action == "correct":
        corrected_concept: str | None = human_response.get("mapped_concept")
        if not corrected_concept:
            logger.warning("HITL 'correct' action has no mapped_concept — treating as approve.")
            return Command(goto="Generate_Cypher")

        corrected_proposal = proposal.model_copy(
            update={"mapped_concept": corrected_concept, "confidence": 1.0}
        )
        logger.info(
            "HITL: human corrected '%s' → '%s'.",
            proposal.mapped_concept, corrected_concept,
        )
        return Command(
            update={"mapping_proposal": corrected_proposal},
            goto="Generate_Cypher",
        )

    if action == "reject":
        logger.info("HITL: human rejected mapping for table '%s'.", proposal.table_name)
        return Command(update={"rejected": True}, goto="End")

    logger.warning("Unknown HITL action '%s' — treating as approve.", action)
    return Command(goto="Generate_Cypher")
```

### Checkpointer setup (called at graph compile time)

```python
# src/graph/builder_graph.py — excerpt showing checkpointer injection
from langgraph.checkpoint.memory import MemorySaver
# from langgraph.checkpoint.sqlite import SqliteSaver  # production

def compile_builder_graph(*, production: bool = False):
    from src.config.settings import get_settings
    settings = get_settings()

    if production:
        # SqliteSaver persists across restarts; path from settings
        checkpointer = SqliteSaver.from_conn_string(settings.sqlite_checkpoint_path)
    else:
        checkpointer = MemorySaver()

    graph = _build_raw_graph()          # StateGraph already built
    return graph.compile(checkpointer=checkpointer, interrupt_before=["hitl_node"])
```

---

## 5. Tests

```python
"""Unit tests for src/mapping/hitl.py — UT-09"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from src.mapping.hitl import (
    HumanAction,
    _CONFIDENCE_THRESHOLD,
    build_interrupt_payload,
    hitl_node,
    should_interrupt,
)
from src.models.schemas import Entity, MappingProposal


# ── Helpers ────────────────────────────────────────────────────────────────────

def _proposal(concept: str = "Customer", confidence: float = 0.95) -> MappingProposal:
    return MappingProposal(
        table_name="TB_CST",
        mapped_concept=concept,
        confidence=confidence,
        reasoning="Looks like customer data.",
        alternative_concepts=["Client"],
    )


def _entity(name: str, prov: str = "Source A") -> Entity:
    return Entity(
        name=name, definition="A definition.",
        synonyms=[], provenance_text=prov, source_doc="test.pdf",
    )


# ── should_interrupt ───────────────────────────────────────────────────────────

class TestShouldInterrupt:
    def test_hitl_flag_true_triggers(self) -> None:
        state = {"hitl_flag": True, "mapping_proposal": _proposal()}
        assert should_interrupt(state) is True

    def test_low_confidence_triggers(self) -> None:
        state = {"hitl_flag": False, "mapping_proposal": _proposal(confidence=0.5)}
        assert should_interrupt(state) is True

    def test_high_confidence_no_flag_no_interrupt(self) -> None:
        state = {"hitl_flag": False, "mapping_proposal": _proposal(confidence=0.95)}
        assert should_interrupt(state) is False

    def test_no_proposal_no_flag_no_interrupt(self) -> None:
        state = {"hitl_flag": False}
        assert should_interrupt(state) is False

    def test_exactly_at_threshold_no_interrupt(self) -> None:
        state = {"hitl_flag": False, "mapping_proposal": _proposal(confidence=_CONFIDENCE_THRESHOLD)}
        assert should_interrupt(state) is False


# ── build_interrupt_payload ────────────────────────────────────────────────────

class TestBuildInterruptPayload:
    def test_required_keys_present(self) -> None:
        prop = _proposal()
        payload = build_interrupt_payload(prop, [_entity("Customer"), _entity("Client")])
        for key in ("table_name", "proposed_concept", "confidence", "reasoning",
                    "alternative_concepts", "provenance_text"):
            assert key in payload

    def test_proposed_excluded_from_alternatives(self) -> None:
        prop = _proposal(concept="Customer")
        entities = [_entity("Customer"), _entity("Client"), _entity("Account")]
        payload = build_interrupt_payload(prop, entities)
        assert "Customer" not in payload["alternative_concepts"]

    def test_alternatives_capped_at_four(self) -> None:
        prop = _proposal()
        entities = [_entity(f"E{i}") for i in range(10)]
        payload = build_interrupt_payload(prop, entities)
        assert len(payload["alternative_concepts"]) <= 4

    def test_provenance_text_joined(self) -> None:
        prop = _proposal()
        entities = [_entity("X", prov="Prov A"), _entity("Y", prov="Prov B")]
        payload = build_interrupt_payload(prop, entities)
        assert "Prov A" in payload["provenance_text"]
        assert "Prov B" in payload["provenance_text"]


# ── hitl_node ─────────────────────────────────────────────────────────────────

class TestHitlNode:
    def _state_high_conf(self) -> dict:
        return {
            "hitl_flag": False,
            "mapping_proposal": _proposal(confidence=0.99),
            "current_entities": [_entity("Customer")],
        }

    def _state_low_conf(self) -> dict:
        return {
            "hitl_flag": False,
            "mapping_proposal": _proposal(confidence=0.5),
            "current_entities": [_entity("Client")],
        }

    def test_pass_through_on_high_confidence(self) -> None:
        cmd = hitl_node(self._state_high_conf())
        assert cmd.goto == "Generate_Cypher"

    def test_approve_routes_to_generate_cypher(self) -> None:
        with patch("src.mapping.hitl.interrupt", return_value={"action": "approve"}):
            cmd = hitl_node(self._state_low_conf())
        assert cmd.goto == "Generate_Cypher"

    def test_correct_updates_proposal(self) -> None:
        with patch("src.mapping.hitl.interrupt", return_value={"action": "correct", "mapped_concept": "Account"}):
            cmd = hitl_node(self._state_low_conf())
        assert cmd.goto == "Generate_Cypher"
        assert cmd.update["mapping_proposal"].mapped_concept == "Account"
        assert cmd.update["mapping_proposal"].confidence == 1.0

    def test_reject_routes_to_end(self) -> None:
        with patch("src.mapping.hitl.interrupt", return_value={"action": "reject"}):
            cmd = hitl_node(self._state_low_conf())
        assert cmd.goto == "End"
        assert cmd.update["rejected"] is True

    def test_unknown_action_defaults_to_approve(self) -> None:
        with patch("src.mapping.hitl.interrupt", return_value={"action": "???"}):
            cmd = hitl_node(self._state_low_conf())
        assert cmd.goto == "Generate_Cypher"

    def test_none_proposal_routes_to_end(self) -> None:
        state = {"hitl_flag": True, "mapping_proposal": None, "current_entities": []}
        cmd = hitl_node(state)
        assert cmd.goto == "End"
```

---

## 6. Smoke Test

```bash
python -c "
from src.mapping.hitl import should_interrupt, build_interrupt_payload
from src.models.schemas import MappingProposal, Entity

p = MappingProposal(
    table_name='TB_PRD',
    mapped_concept='Product',
    confidence=0.75,
    reasoning='Contains product_id and price.',
    alternative_concepts=['Item', 'SKU'],
)
e = Entity(
    name='Product', definition='A sellable good.',
    synonyms=['Item'], provenance_text='Sales DDL', source_doc='ddl.sql',
)

state = {'hitl_flag': False, 'mapping_proposal': p, 'current_entities': [e]}
print('should_interrupt (conf=0.75):', should_interrupt(state))

payload = build_interrupt_payload(p, [e])
print('Payload keys:', list(payload.keys()))
print('Alternatives:', payload['alternative_concepts'])
"
```
