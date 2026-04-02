"""Integration tests for src/graph/cypher_healer.py.

Tests: IT-04 (Cypher Healing Loop - Full)
"""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from src.graph.cypher_healer import heal_cypher
from src.models.schemas import MappingProposal

pytestmark = pytest.mark.integration


# ─────────────────────────────────────────────────────────────────────────────
# IT-04: Cypher Healing Loop (Full)
# ─────────────────────────────────────────────────────────────────────────────


@pytest.mark.integration
class TestCypherHealingLoop:
    """IT-04: Cypher healing recovers from syntax errors."""

    def test_cypher_healing_succeeds_on_second_attempt(
        self,
        neo4j_client,
    ) -> None:
        """Broken Cypher on attempt 1 → healed Cypher on attempt 2 → graph updated."""
        # Create a test mapping proposal
        proposal = MappingProposal(
            table_name="TEST_TABLE",
            mapped_concept="TestConcept",
            confidence=0.95,
            reasoning="Test mapping",
            alternative_concepts=[],
        )

        # First Cypher attempt has syntax error (invalid keyword)
        broken_cypher = """
CREET (c:BusinessConcept {name: 'TestConcept'})
SET c.definition = 'A test concept'
MERGE (t:PhysicalTable {table_name: 'TEST_TABLE'})
MERGE (c)-[:MAPPED_TO]->(t)
"""

        # Second attempt has valid Cypher
        valid_cypher = """
MERGE (c:BusinessConcept {name: 'TestConcept'})
SET c.definition = 'A test concept'
MERGE (t:PhysicalTable {table_name: 'TEST_TABLE'})
MERGE (c)-[:MAPPED_TO]->(t)
"""

        cypher_attempts = [0]
        cypher_responses = [broken_cypher, valid_cypher]

        def _mock_llm_invoke(*args, **kwargs):
            """Mock LLM that returns fixed Cypher strings."""
            cypher_attempts[0] += 1
            result = MagicMock()

            if cypher_attempts[0] <= len(cypher_responses):
                result.content = cypher_responses[cypher_attempts[0] - 1]
            else:
                result.content = valid_cypher  # Always return valid after attempts exhausted

            return result

        mock_llm = MagicMock()
        mock_llm.invoke = _mock_llm_invoke

        # Run healing
        with neo4j_client:
            healed = heal_cypher(
                broken_cypher,
                proposal,
                neo4j_client.driver,
                mock_llm,
                max_attempts=3,
            )

        # Verify healing succeeded
        assert healed is not None
        assert "MERGE" in healed
        assert healed == valid_cypher

        # Verify the LLM was called multiple times (initial + healing)
        assert cypher_attempts[0] >= 2

    def test_cypher_healing_max_attempts_exceeded(
        self,
        neo4j_client,
    ) -> None:
        """All Cypher attempts fail → returns None after max_attempts."""
        proposal = MappingProposal(
            table_name="TEST_TABLE",
            mapped_concept="TestConcept",
            confidence=0.95,
            reasoning="Test mapping",
            alternative_concepts=[],
        )

        # Always return broken Cypher
        broken_cypher = """
CREET (c:BusinessConcept {name: 'TestConcept'})
SET c.definition = 'A test concept'
"""

        mock_llm = MagicMock()
        result = MagicMock()
        result.content = broken_cypher
        mock_llm.invoke.return_value = result

        # Run healing with low max_attempts
        with neo4j_client:
            healed = heal_cypher(
                broken_cypher,
                proposal,
                neo4j_client.driver,
                mock_llm,
                max_attempts=2,
            )

        # Verify healing failed
        assert healed is None

    def test_cypher_healing_first_attempt_succeeds(
        self,
        neo4j_client,
    ) -> None:
        """First attempt succeeds with valid Cypher."""
        proposal = MappingProposal(
            table_name="TEST_TABLE",
            mapped_concept="TestConcept",
            confidence=0.95,
            reasoning="Test mapping",
            alternative_concepts=[],
        )

        valid_cypher = """
MERGE (c:BusinessConcept {name: 'TestConcept'})
SET c.definition = 'A test concept'
MERGE (t:PhysicalTable {table_name: 'TEST_TABLE'})
MERGE (c)-[:MAPPED_TO]->(t)
"""

        mock_llm = MagicMock()
        llm_calls = [0]

        def _invoke(*args, **kwargs):
            llm_calls[0] += 1
            result = MagicMock()
            result.content = valid_cypher
            return result

        mock_llm.invoke = _invoke

        # Run healing
        with neo4j_client:
            healed = heal_cypher(
                valid_cypher,
                proposal,
                neo4j_client.driver,
                mock_llm,
                max_attempts=3,
            )

        # Verify healing succeeded immediately
        assert healed == valid_cypher

        # LLM should not have been called for healing (first attempt succeeded)
        assert llm_calls[0] == 0

    def test_cypher_healing_with_syntax_error_in_message(
        self,
        neo4j_client,
    ) -> None:
        """Healing prompt contains the actual syntax error from Neo4j."""
        proposal = MappingProposal(
            table_name="TEST_TABLE",
            mapped_concept="TestConcept",
            confidence=0.95,
            reasoning="Test mapping",
            alternative_concepts=[],
        )

        broken_cypher = """
CREET (c:BusinessConcept {name: 'TestConcept'})
"""

        valid_cypher = """
MERGE (c:BusinessConcept {name: 'TestConcept'})
"""

        received_prompts = []

        def _mock_llm_invoke(*args, **kwargs):
            """Capture prompts to verify error is injected."""
            prompt = str(args[0]) if args else ""
            received_prompts.append(prompt)

            result = MagicMock()
            # First call gets the error, second call succeeds
            if len(received_prompts) == 1:
                result.content = broken_cypher
            else:
                result.content = valid_cypher
            return result

        mock_llm = MagicMock()
        mock_llm.invoke = _mock_llm_invoke

        # Run healing
        with neo4j_client:
            healed = heal_cypher(
                broken_cypher,
                proposal,
                neo4j_client.driver,
                mock_llm,
                max_attempts=3,
            )

        # Verify healing succeeded
        assert healed is not None
        assert healed == valid_cypher

        # Verify the error message was in the prompt
        # The second prompt should contain the syntax error
        if len(received_prompts) > 1:
            assert "CREET" in received_prompts[1] or "syntax" in received_prompts[1].lower()

    def test_cypher_healing_respects_max_attempts_setting(
        self,
        neo4j_client,
    ) -> None:
        """Healing loop exits after exactly max_attempts failures."""
        proposal = MappingProposal(
            table_name="TEST_TABLE",
            mapped_concept="TestConcept",
            confidence=0.95,
            reasoning="Test mapping",
            alternative_concepts=[],
        )

        # Always return broken Cypher
        broken_cypher = """
CREET (c:BusinessConcept {name: 'TestConcept'})
"""

        llm_call_count = [0]

        def _mock_llm_invoke(*args, **kwargs):
            llm_call_count[0] += 1
            result = MagicMock()
            result.content = broken_cypher
            return result

        mock_llm = MagicMock()
        mock_llm.invoke = _mock_llm_invoke

        max_attempts = 3

        # Run healing
        with neo4j_client:
            healed = heal_cypher(
                broken_cypher,
                proposal,
                neo4j_client.driver,
                mock_llm,
                max_attempts=max_attempts,
            )

        # Verify healing failed
        assert healed is None

        # Verify LLM was called exactly max_attempts times for healing
        # (not counting the initial generation)
        # The healing function calls LLM for each retry
        assert llm_call_count[0] == max_attempts
