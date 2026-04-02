"""Unit tests for src/models/state.py"""

from __future__ import annotations

from src.models.state import BuilderState, QueryState


class TestBuilderState:
    def test_partial_init(self) -> None:
        # TypedDict with total=False allows any subset of keys
        state: BuilderState = {"documents": [], "ingestion_errors": []}
        assert state["documents"] == []
        assert state["ingestion_errors"] == []

    def test_empty_init(self) -> None:
        state: BuilderState = {}
        assert len(state) == 0

    def test_can_set_hitl_flag(self) -> None:
        state: BuilderState = {"hitl_flag": True}
        assert state["hitl_flag"] is True

    def test_can_accumulate_errors(self) -> None:
        state: BuilderState = {"ingestion_errors": []}
        state["ingestion_errors"].append("PDF load failed: file not found")
        assert len(state["ingestion_errors"]) == 1

    def test_mapping_queue_fields(self) -> None:
        state: BuilderState = {
            "pending_tables": [],
            "current_table": None,
            "mapping_proposal": None,
            "reflection_attempts": 0,
        }
        assert state["current_table"] is None
        assert state["reflection_attempts"] == 0


class TestQueryState:
    def test_user_query_only(self) -> None:
        state: QueryState = {"user_query": "What is a Customer?"}
        assert state["user_query"] == "What is a Customer?"

    def test_defaults_to_empty(self) -> None:
        state: QueryState = {}
        # 'final_answer' key not present — access should raise KeyError
        assert "final_answer" not in state

    def test_iteration_counter(self) -> None:
        state: QueryState = {"user_query": "Q", "iteration_count": 0}
        state["iteration_count"] += 1
        assert state["iteration_count"] == 1

    def test_full_workflow_fields(self) -> None:
        from src.models.schemas import GraderDecision, RetrievedChunk

        rc = RetrievedChunk(
            node_id="bc-1",
            node_type="BusinessConcept",
            text="Customer: end user",
            score=0.95,
            source_type="vector",
        )
        gd = GraderDecision(grounded=True, action="pass")
        state: QueryState = {
            "user_query": "Q",
            "retrieved_chunks": [rc],
            "reranked_chunks": [rc],
            "current_answer": "A Customer is an end user.",
            "last_critique": None,
            "grader_decision": gd,
            "final_answer": "A Customer is an end user.",
            "sources": ["bc-1"],
            "iteration_count": 1,
        }
        assert state["grader_decision"].grounded is True
        assert state["sources"] == ["bc-1"]
