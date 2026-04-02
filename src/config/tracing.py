"""Pipeline tracing infrastructure for end-to-end data flow analysis.

This module provides data structures and utilities for tracing the complete
execution flow through both Builder and Query graphs, enabling detailed
post-hoc analysis of pipeline behavior.

Usage:
    from src.config.tracing import BuilderTrace, QueryTrace, save_trace

    # During builder execution
    trace = BuilderTrace.create(study_id="AB-00", settings=settings)
    trace.record_chunks(chunks)
    trace.record_triplets(triplets)
    # ... record other stages
    save_trace(trace, output_dir)

    # During query execution
    query_trace = QueryTrace.create(study_id="AB-00", question=question, builder_trace_id=trace.id)
    query_trace.record_retrieval(vector_results, bm25_results, graph_results)
    query_trace.record_reranking(pre_rerank, post_rerank)
    # ... record other stages
    save_trace(query_trace, output_dir)
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

# ─────────────────────────────────────────────────────────────────────────────
# Tracing Configuration
# ─────────────────────────────────────────────────────────────────────────────

TRUNCATE_LENGTH = 500  # Max length for text fields (prevent huge trace files)
MAX_ITEMS = 100  # Max items to keep per list (prevent memory issues)


def truncate_text(text: str, max_length: int = TRUNCATE_LENGTH) -> str:
    """Truncate text to max length, adding indicator if truncated."""
    if not text or len(text) <= max_length:
        return text
    return text[:max_length] + "... [TRUNCATED]"


def truncate_list(items: list[Any], max_items: int = MAX_ITEMS) -> list[Any]:
    """Truncate list to max items, adding indicator if truncated."""
    if not items or len(items) <= max_items:
        return items
    return items[:max_items] + [f"... [{len(items) - max_items} more items TRUNCATED]"]


# ─────────────────────────────────────────────────────────────────────────────
# Builder Trace
# ─────────────────────────────────────────────────────────────────────────────


@dataclass
class BuilderTrace:
    """Complete trace of Builder Graph execution.

    Records the state of the pipeline at each major stage:
    - Input documents and DDL files
    - Chunks generated from documents
    - Triplets extracted from chunks
    - Entity resolution process
    - Schema-to-ontology mapping
    - Cypher generation and graph building
    """

    # Metadata
    study_id: str
    timestamp: str
    trace_id: str = field(default="")
    config: dict[str, Any] = field(default_factory=dict)

    # Input
    source_documents: list[str] = field(default_factory=list)
    ddl_files: list[str] = field(default_factory=list)

    # Chunking
    chunks: list[dict[str, Any]] = field(default_factory=list)
    chunking_summary: dict[str, Any] = field(default_factory=dict)

    # Extraction
    triplets: list[dict[str, Any]] = field(default_factory=list)
    extraction_summary: dict[str, Any] = field(default_factory=dict)

    # Entity Resolution
    entities_pre_resolution: list[dict[str, Any]] = field(default_factory=list)
    blocks: list[dict[str, Any]] = field(default_factory=list)
    cluster_decisions: list[dict[str, Any]] = field(default_factory=list)
    entities_post_resolution: list[dict[str, Any]] = field(default_factory=list)
    resolution_summary: dict[str, Any] = field(default_factory=dict)

    # Schema Processing
    tables_parsed: list[dict[str, Any]] = field(default_factory=list)
    tables_enriched: list[dict[str, Any]] = field(default_factory=list)
    schema_summary: dict[str, Any] = field(default_factory=dict)

    # Mapping
    table_mappings: list[dict[str, Any]] = field(default_factory=list)
    mapping_summary: dict[str, Any] = field(default_factory=dict)

    # Cypher & Graph
    cypher_queries: list[dict[str, Any]] = field(default_factory=list)
    neo4j_summary: dict[str, Any] = field(default_factory=dict)

    # Timing
    stage_timings: dict[str, float] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Generate trace_id if not provided."""
        if not self.trace_id:
            self.trace_id = f"{self.study_id}.{self.timestamp.replace(':', '-')}"

    @classmethod
    def create(
        cls,
        study_id: str,
        settings: object | None = None,
        doc_paths: list[Path] | None = None,
        ddl_paths: list[Path] | None = None,
    ) -> BuilderTrace:
        """Create a new BuilderTrace with initial metadata."""
        timestamp = datetime.now(UTC).isoformat()
        trace = cls(study_id=study_id, timestamp=timestamp)

        # Record settings
        if settings:
            trace.config = {
                "llm_model_reasoning": getattr(settings, "llm_model_reasoning", ""),
                "llm_model_extraction": getattr(settings, "llm_model_extraction", ""),
                "chunk_size": getattr(settings, "chunk_size", 0),
                "chunk_overlap": getattr(settings, "chunk_overlap", 0),
                "er_similarity_threshold": getattr(settings, "er_similarity_threshold", 0.0),
                "er_blocking_top_k": getattr(settings, "er_blocking_top_k", 0),
                "enable_schema_enrichment": getattr(settings, "enable_schema_enrichment", False),
                "enable_critic_validation": getattr(settings, "enable_critic_validation", False),
                "enable_cypher_healing": getattr(settings, "enable_cypher_healing", False),
                "retrieval_mode": getattr(settings, "retrieval_mode", ""),
                "enable_reranker": getattr(settings, "enable_reranker", False),
            }

        # Record input files
        if doc_paths:
            trace.source_documents = [str(p) for p in doc_paths]
        if ddl_paths:
            trace.ddl_files = [str(p) for p in ddl_paths]

        return trace

    def record_chunks(self, chunks: list[dict[str, Any]]) -> None:
        """Record chunks generated from documents."""
        truncated_chunks = []
        for chunk in chunks:
            truncated_chunks.append(
                {
                    "chunk_id": chunk.get("chunk_id", ""),
                    "text": truncate_text(chunk.get("text", "")),
                    "source": chunk.get("source", ""),
                    "page": chunk.get("page", 0),
                    "token_count": chunk.get("token_count", 0),
                }
            )
        self.chunks = truncate_list(truncated_chunks)
        self.chunking_summary = {
            "total_chunks": len(chunks),
            "total_tokens": sum(int(c.get("token_count", 0) or 0) for c in chunks),
            "avg_tokens": sum(int(c.get("token_count", 0) or 0) for c in chunks) / len(chunks)
            if chunks
            else 0,
        }

    def record_triplets(
        self, triplets: list[dict[str, Any]], extraction_errors: list[dict[str, Any]] | None = None
    ) -> None:
        """Record triplets extracted from chunks."""
        truncated_triplets = []
        for t in triplets:
            truncated_triplets.append(
                {
                    "chunk_index": t.get("chunk_index", -1),
                    "subject": truncate_text(t.get("subject", ""), 100),
                    "predicate": truncate_text(t.get("predicate", ""), 100),
                    "object": truncate_text(t.get("object", ""), 100),
                    "confidence": t.get("confidence", 0.0),
                }
            )
        self.triplets = truncate_list(truncated_triplets)
        self.extraction_summary = {
            "total_triplets": len(triplets),
            "avg_confidence": sum(t.get("confidence", 0.0) for t in triplets) / len(triplets)
            if triplets
            else 0.0,
            "extraction_errors": len(extraction_errors) if extraction_errors else 0,
        }

    def record_entity_resolution(
        self,
        entities_pre: list[dict[str, Any]],
        blocks: list[dict[str, Any]],
        decisions: list[dict[str, Any]],
        entities_post: list[dict[str, Any]],
    ) -> None:
        """Record entity resolution process."""
        # Pre-resolution entities (raw from triplets)
        self.entities_pre_resolution = truncate_list(
            [
                {
                    "name": truncate_text(e.get("name", ""), 100),
                    "provenance": e.get("provenance", ""),
                }
                for e in entities_pre
            ]
        )

        # Blocking results
        self.blocks = truncate_list(
            [
                {
                    "block_id": b.get("block_id", ""),
                    "entity_count": len(b.get("entities", [])),
                    "avg_similarity": b.get("avg_similarity", 0.0),
                }
                for b in blocks
            ]
        )

        # LLM judge decisions
        self.cluster_decisions = truncate_list(
            [
                {
                    "cluster_id": d.get("cluster_id", ""),
                    "decision": d.get("decision", ""),
                    "reasoning": truncate_text(d.get("reasoning", ""), 200),
                }
                for d in decisions
            ]
        )

        # Post-resolution entities (canonical)
        self.entities_post_resolution = truncate_list(
            [
                {
                    "name": truncate_text(e.get("name", ""), 100),
                    "definition": truncate_text(e.get("definition", ""), 200),
                    "synonyms": e.get("synonyms", [])[:5],  # Limit synonyms
                }
                for e in entities_post
            ]
        )

        self.resolution_summary = {
            "entities_pre": len(entities_pre),
            "entities_post": len(entities_post),
            "blocks_created": len(blocks),
            "decisions_made": len(decisions),
            "reduction_rate": 1.0 - (len(entities_post) / len(entities_pre))
            if entities_pre
            else 0.0,
        }

    def record_schema_processing(
        self,
        tables: list[dict[str, Any]],
        enriched_tables: list[dict[str, Any]] | None = None,
    ) -> None:
        """Record DDL parsing and schema enrichment."""
        self.tables_parsed = truncate_list(
            [{"name": t.get("name", ""), "columns": len(t.get("columns", []))} for t in tables]
        )

        if enriched_tables:
            self.tables_enriched = truncate_list(
                [
                    {
                        "name": t.get("name", ""),
                        "description": truncate_text(t.get("description", ""), 200),
                    }
                    for t in enriched_tables
                ]
            )

        self.schema_summary = {
            "tables_parsed": len(tables),
            "tables_enriched": len(enriched_tables) if enriched_tables else 0,
            "total_columns": sum(len(t.get("columns", [])) for t in tables),
        }

    def record_mapping(self, mappings: list[dict[str, Any]]) -> None:
        """Record schema-to-ontology mapping results."""
        self.table_mappings = truncate_list(
            [
                {
                    "table": m.get("table", ""),
                    "concept": m.get("concept", ""),
                    "confidence": m.get("confidence", 0.0),
                    "alternatives": m.get("alternatives", [])[:3],  # Top 3 alternatives
                }
                for m in mappings
            ]
        )

        if mappings:
            confidences = [m.get("confidence", 0.0) for m in mappings]
            self.mapping_summary = {
                "tables_mapped": len(mappings),
                "avg_confidence": sum(confidences) / len(confidences),
                "min_confidence": min(confidences),
                "max_confidence": max(confidences),
                "low_confidence_count": sum(1 for c in confidences if c < 0.7),
            }

    def record_cypher_and_graph(
        self,
        cypher_results: list[dict[str, Any]],
        neo4j_stats: dict[str, int] | None = None,
    ) -> None:
        """Record Cypher generation and graph building."""
        self.cypher_queries = truncate_list(
            [
                {
                    "table": c.get("table", ""),
                    "success": c.get("success", False),
                    "healing_attempts": c.get("healing_attempts", 0),
                    "cypher_preview": truncate_text(c.get("cypher", ""), 200),
                }
                for c in cypher_results
            ]
        )

        self.neo4j_summary = {
            "queries_executed": len(cypher_results),
            "successful_queries": sum(1 for c in cypher_results if c.get("success", False)),
            "healing_triggered": sum(1 for c in cypher_results if c.get("healing_attempts", 0) > 0),
            "total_healing_attempts": sum(c.get("healing_attempts", 0) for c in cypher_results),
        }

        if neo4j_stats:
            self.neo4j_summary.update(neo4j_stats)

    def record_timing(self, stage: str, duration_seconds: float) -> None:
        """Record timing for a pipeline stage."""
        self.stage_timings[stage] = duration_seconds

    def to_dict(self) -> dict[str, Any]:
        """Convert to JSON-serializable dict."""
        return asdict(self)

    def save(self, output_dir: Path) -> Path:
        """Save trace to JSON file."""
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / f"builder_trace_{self.trace_id}.json"

        with open(output_file, "w") as f:
            json.dump(self.to_dict(), f, indent=2, default=str)

        return output_file


# ─────────────────────────────────────────────────────────────────────────────
# Query Trace
# ─────────────────────────────────────────────────────────────────────────────


@dataclass
class QueryTrace:
    """Complete trace of a single Query Graph execution.

    Records the state of the query pipeline at each major stage:
    - Hybrid retrieval (vector, BM25, graph traversal)
    - Reranking
    - Context preparation
    - Answer generation with retries
    - Hallucination grading
    """

    # Metadata
    study_id: str
    question: str
    timestamp: str
    trace_id: str = field(default="")
    builder_trace_id: str = field(default="")
    query_index: int = -1

    # Retrieval
    query_embedding: dict[str, Any] = field(default_factory=dict)
    vector_results: list[dict[str, Any]] = field(default_factory=list)
    bm25_results: list[dict[str, Any]] = field(default_factory=list)
    graph_traversal_results: list[dict[str, Any]] = field(default_factory=list)
    rrf_fused: list[dict[str, Any]] = field(default_factory=list)
    retrieval_summary: dict[str, Any] = field(default_factory=dict)

    # Reranking
    pre_rerank: list[dict[str, Any]] = field(default_factory=list)
    post_rerank: list[dict[str, Any]] = field(default_factory=list)
    reranker_summary: dict[str, Any] = field(default_factory=dict)

    # Context Preparation
    contexts_for_generation: list[dict[str, Any]] = field(default_factory=list)
    context_summary: dict[str, Any] = field(default_factory=dict)

    # Generation
    generation_attempts: list[dict[str, Any]] = field(default_factory=list)
    generation_summary: dict[str, Any] = field(default_factory=dict)

    # Output
    final_answer: str = ""
    grounded: bool = False
    verification_score: float = 0.0
    halluncination_grader_decision: str = ""
    sources: list[str] = field(default_factory=list)

    # Timing
    stage_timings: dict[str, float] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Generate trace_id if not provided."""
        if not self.trace_id:
            self.trace_id = (
                f"{self.study_id}.Q{self.query_index}.{self.timestamp.replace(':', '-')}"
            )

    @classmethod
    def create(
        cls,
        study_id: str,
        question: str,
        query_index: int,
        builder_trace_id: str = "",
    ) -> QueryTrace:
        """Create a new QueryTrace."""
        timestamp = datetime.now(UTC).isoformat()
        return cls(
            study_id=study_id,
            question=question,
            timestamp=timestamp,
            query_index=query_index,
            builder_trace_id=builder_trace_id,
        )

    def record_retrieval(
        self,
        vector_results: list[dict[str, Any]] | None = None,
        bm25_results: list[dict[str, Any]] | None = None,
        graph_results: list[dict[str, Any]] | None = None,
        rrf_fused: list[dict[str, Any]] | None = None,
    ) -> None:
        """Record hybrid retrieval results."""
        if vector_results:
            self.vector_results = truncate_list(
                [{"node": r.get("node", ""), "score": r.get("score", 0.0)} for r in vector_results]
            )

        if bm25_results:
            self.bm25_results = truncate_list(
                [{"node": r.get("node", ""), "score": r.get("score", 0.0)} for r in bm25_results]
            )

        if graph_results:
            self.graph_traversal_results = truncate_list(
                [{"node": r.get("node", ""), "depth": r.get("depth", 0)} for r in graph_results]
            )

        if rrf_fused:
            self.rrf_fused = truncate_list(
                [
                    {
                        "node": r.get("node", ""),
                        "rrf_score": r.get("rrf_score", 0.0),
                        "sources": r.get("sources", []),
                    }
                    for r in rrf_fused
                ]
            )

        self.retrieval_summary = {
            "vector_count": len(vector_results) if vector_results else 0,
            "bm25_count": len(bm25_results) if bm25_results else 0,
            "graph_count": len(graph_results) if graph_results else 0,
            "fused_count": len(rrf_fused) if rrf_fused else 0,
        }

    def record_reranking(
        self,
        pre_rerank: list[dict[str, Any]],
        post_rerank: list[dict[str, Any]],
        model: str = "",
    ) -> None:
        """Record reranking results."""
        self.pre_rerank = truncate_list(
            [{"node": r.get("node", ""), "score": r.get("score", 0.0)} for r in pre_rerank]
        )

        self.post_rerank = truncate_list(
            [
                {
                    "node": r.get("node", ""),
                    "score": r.get("score", 0.0),
                    "score_delta": r.get("score", 0.0) - pre_rerank[i].get("score", 0.0)
                    if i < len(pre_rerank)
                    else 0.0,
                }
                for i, r in enumerate(post_rerank)
            ]
        )

        # Calculate rank changes
        pre_ranks = {r.get("node", ""): i for i, r in enumerate(pre_rerank)}
        post_ranks = {r.get("node", ""): i for i, r in enumerate(post_rerank)}
        rank_changes = [
            pre_ranks.get(n, 999) - post_ranks.get(n, 999) for n in post_ranks if n in pre_ranks
        ]

        self.reranker_summary = {
            "model": model,
            "pre_count": len(pre_rerank),
            "post_count": len(post_rerank),
            "avg_rank_change": sum(rank_changes) / len(rank_changes) if rank_changes else 0.0,
            "max_rank_improvement": max(rank_changes) if rank_changes else 0.0,
        }

    def record_context_preparation(
        self,
        contexts: list[dict[str, Any]],
        context_limit: int | None = None,
    ) -> None:
        """Record contexts prepared for generation."""
        self.contexts_for_generation = truncate_list(
            [
                {
                    "node": c.get("node", ""),
                    "text": truncate_text(c.get("text", "")),
                    "source": c.get("source", "unknown"),
                }
                for c in contexts
            ]
        )

        total_chars = sum(len(c.get("text", "")) for c in contexts)
        self.context_summary = {
            "contexts_used": len(contexts),
            "total_characters": total_chars,
            "context_limit": context_limit,
            "truncated": len(contexts) > context_limit if context_limit else False,
        }

    def record_generation_attempt(
        self,
        answer: str,
        critique: str = "",
        grader_decision: str = "",
        attempt_number: int = 1,
    ) -> None:
        """Record a single generation attempt."""
        self.generation_attempts.append(
            {
                "attempt": attempt_number,
                "answer": truncate_text(answer),
                "critique": truncate_text(critique),
                "grader_decision": grader_decision,
            }
        )

    def record_generation_summary(self) -> None:
        """Generate summary from generation attempts."""
        if self.generation_attempts:
            self.generation_summary = {
                "total_attempts": len(self.generation_attempts),
                "final_decision": self.generation_attempts[-1].get("grader_decision", ""),
            }

    def record_output(
        self,
        answer: str,
        grounded: bool,
        verification_score: float,
        grader_decision: str,
        sources: list[str],
    ) -> None:
        """Record final output."""
        self.final_answer = truncate_text(answer, 1000)
        self.grounded = grounded
        self.verification_score = verification_score
        self.halluncination_grader_decision = grader_decision
        self.sources = sources

    def record_timing(self, stage: str, duration_seconds: float) -> None:
        """Record timing for a pipeline stage."""
        self.stage_timings[stage] = duration_seconds

    def to_dict(self) -> dict[str, Any]:
        """Convert to JSON-serializable dict."""
        return asdict(self)

    def save(self, output_file: Path) -> Path:
        """Append trace to JSONL file."""
        output_file.parent.mkdir(parents=True, exist_ok=True)

        # Open in append mode for JSONL
        with open(output_file, "a") as f:
            f.write(json.dumps(self.to_dict(), default=str) + "\n")

        return output_file


# ─────────────────────────────────────────────────────────────────────────────
# Comparison Report
# ─────────────────────────────────────────────────────────────────────────────


@dataclass
class ComparisonReport:
    """Report comparing retrieved contexts with ground truth."""

    study_id: str
    timestamp: str
    dataset_path: str = ""

    # Per-question analysis
    per_question_analysis: list[dict[str, Any]] = field(default_factory=list)

    # Aggregate metrics
    aggregate_metrics: dict[str, Any] = field(default_factory=dict)

    # Bottleneck identification
    bottlenecks: list[dict[str, Any]] = field(default_factory=list)

    # Recommendations
    recommendations: list[str] = field(default_factory=list)

    def generate_per_question_analysis(
        self,
        query_traces: list[QueryTrace],
        ground_truth: list[dict[str, Any]],
    ) -> None:
        """Generate per-question comparison."""
        for i, (trace, gt) in enumerate(zip(query_traces, ground_truth)):
            retrieved_nodes = [r.get("node", "") for r in trace.post_rerank or trace.rrf_fused]
            expected_sources = gt.get("expected_sources", [])

            # Check coverage
            covered = [s for s in expected_sources if any(s in node for node in retrieved_nodes)]
            missing = [
                s for s in expected_sources if not any(s in node for node in retrieved_nodes)
            ]

            self.per_question_analysis.append(
                {
                    "query_index": i,
                    "question": truncate_text(gt.get("question", ""), 100),
                    "expected_sources": expected_sources,
                    "retrieved_nodes": retrieved_nodes[:10],  # Top 10
                    "covered_sources": covered,
                    "missing_sources": missing,
                    "coverage_rate": len(covered) / len(expected_sources)
                    if expected_sources
                    else 1.0,
                    "grounded": trace.grounded,
                    "verification_score": trace.verification_score,
                }
            )

    def generate_aggregate_metrics(self) -> None:
        """Generate aggregate metrics from per-question analysis."""
        if not self.per_question_analysis:
            return

        coverage_rates = [q["coverage_rate"] for q in self.per_question_analysis]
        grounded_count = sum(1 for q in self.per_question_analysis if q["grounded"])
        verification_scores = [q["verification_score"] for q in self.per_question_analysis]

        self.aggregate_metrics = {
            "total_questions": len(self.per_question_analysis),
            "avg_coverage_rate": sum(coverage_rates) / len(coverage_rates)
            if coverage_rates
            else 0.0,
            "min_coverage_rate": min(coverage_rates) if coverage_rates else 0.0,
            "grounded_rate": grounded_count / len(self.per_question_analysis)
            if self.per_question_analysis
            else 0.0,
            "avg_verification_score": sum(verification_scores) / len(verification_scores)
            if verification_scores
            else 0.0,
        }

    def identify_bottlenecks(self) -> None:
        """Identify potential bottlenecks based on metrics."""
        bottlenecks = []

        # Coverage bottleneck
        if self.aggregate_metrics.get("avg_coverage_rate", 1.0) < 0.8:
            bottlenecks.append(
                {
                    "type": "retrieval_coverage",
                    "severity": "high"
                    if self.aggregate_metrics["avg_coverage_rate"] < 0.6
                    else "medium",
                    "description": f"Low source coverage rate: {self.aggregate_metrics['avg_coverage_rate']:.2%}",
                }
            )

        # Grounding bottleneck
        if self.aggregate_metrics.get("grounded_rate", 1.0) < 0.9:
            bottlenecks.append(
                {
                    "type": "answer_grounding",
                    "severity": "high"
                    if self.aggregate_metrics["grounded_rate"] < 0.7
                    else "medium",
                    "description": f"Low grounding rate: {self.aggregate_metrics['grounded_rate']:.2%}",
                }
            )

        # Check per-question issues
        low_coverage_questions = [q for q in self.per_question_analysis if q["coverage_rate"] < 0.5]
        if low_coverage_questions:
            bottlenecks.append(
                {
                    "type": "specific_questions",
                    "severity": "medium",
                    "description": f"{len(low_coverage_questions)} questions with < 50% source coverage",
                    "affected_questions": [q["query_index"] for q in low_coverage_questions],
                }
            )

        self.bottlenecks = bottlenecks

    def generate_recommendations(self) -> None:
        """Generate recommendations based on bottlenecks."""
        recommendations = []

        for bottleneck in self.bottlenecks:
            btype = bottleneck["type"]

            if btype == "retrieval_coverage":
                recommendations.append(
                    "Consider increasing RETRIEVAL_VECTOR_TOP_K or RETRIEVAL_BM25_TOP_K "
                    "to improve source coverage."
                )
            elif btype == "answer_grounding":
                recommendations.append(
                    "Review answer generation prompts and context distillation. "
                    "Consider lowering context length limits or improving context selection."
                )
            elif btype == "specific_questions":
                recommendations.append(
                    f"Questions {bottleneck.get('affected_questions', [])} may require "
                    "improved entity mapping or additional business glossary entries."
                )

        self.recommendations = recommendations

    def to_markdown(self) -> str:
        """Generate markdown report."""
        lines = [
            "# AB-00 End-to-End Analysis Report",
            "",
            f"**Study ID**: {self.study_id}",
            f"**Timestamp**: {self.timestamp}",
            f"**Dataset**: {self.dataset_path}",
            "",
            "## Aggregate Metrics",
            "",
        ]

        for key, value in self.aggregate_metrics.items():
            if isinstance(value, float):
                lines.append(f"- **{key}**: {value:.4f}")
            else:
                lines.append(f"- **{key}**: {value}")

        lines.extend(
            [
                "",
                "## Bottlenecks Identified",
                "",
            ]
        )

        for b in self.bottlenecks:
            lines.extend(
                [
                    f"### {b['type'].replace('_', ' ').title()} ({b['severity'].upper()})",
                    f"{b['description']}",
                    "",
                ]
            )

        lines.extend(
            [
                "## Recommendations",
                "",
            ]
        )

        for i, rec in enumerate(self.recommendations, 1):
            lines.append(f"{i}. {rec}")

        lines.extend(
            [
                "",
                "## Per-Question Analysis",
                "",
                "| Index | Question | Coverage | Grounded | Verification |",
                "|-------|----------|----------|----------|--------------|",
            ]
        )

        for q in self.per_question_analysis:
            question = q["question"][:50] + "..." if len(q["question"]) > 50 else q["question"]
            lines.append(
                f"| {q['query_index']} | {question} | {q['coverage_rate']:.2%} | "
                f"{'✓' if q['grounded'] else '✗'} | {q['verification_score']:.3f} |"
            )

        return "\n".join(lines)

    def save(self, output_dir: Path) -> Path:
        """Save report to markdown file."""
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / f"comparison_report_{self.study_id}.md"

        with open(output_file, "w") as f:
            f.write(self.to_markdown())

        return output_file


# ─────────────────────────────────────────────────────────────────────────────
# Utility Functions
# ─────────────────────────────────────────────────────────────────────────────


def save_trace(
    trace: BuilderTrace | QueryTrace,
    output_dir: Path,
) -> Path:
    """Save a trace object to file."""
    return trace.save(output_dir)


def load_builder_trace(trace_file: Path) -> BuilderTrace:
    """Load a builder trace from JSON file."""
    with open(trace_file) as f:
        data = json.load(f)

    # Reconstruct BuilderTrace from dict
    return BuilderTrace(**data)


def load_query_traces(trace_file: Path) -> list[QueryTrace]:
    """Load query traces from JSONL file."""
    traces = []
    with open(trace_file) as f:
        for line in f:
            if line.strip():
                data = json.loads(line)
                traces.append(QueryTrace(**data))
    return traces
