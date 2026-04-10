// TypeScript types mirroring src/api/models.py Pydantic models EXACTLY

// ── LLM Provider ────────────────────────────────────────────────────────────
export type LLMProvider =
  | "auto"
  | "openrouter"
  | "openai"
  | "anthropic"
  | "lmstudio"
  | "ollama"
  | "groq"
  | "google"
  | "bedrock"
  | "azure"
  | "mistral"
  | "together"
  | "deepseek"
  | "xai"
  | "nvidia"
  | "huggingface";

export type RetrievalMode = "hybrid" | "vector" | "bm25";

// ── PipelineConfig ──────────────────────────────────────────────────────────
export interface PipelineConfig {
  provider?: LLMProvider | null;
  reasoning_model?: string | null;
  extraction_model?: string | null;
  midtier_model?: string | null;
  lmstudio_base_url?: string | null;
  temperature_extraction?: number | null;
  temperature_reasoning?: number | null;
  temperature_generation?: number | null;
  max_tokens_extraction?: number | null;
  max_tokens_reasoning?: number | null;
  chunk_size?: number | null;
  chunk_overlap?: number | null;
  parent_chunk_size?: number | null;
  parent_chunk_overlap?: number | null;
  retrieval_mode?: RetrievalMode | null;
  retrieval_vector_top_k?: number | null;
  retrieval_bm25_top_k?: number | null;
  enable_reranker?: boolean | null;
  reranker_top_k?: number | null;
  er_similarity_threshold?: number | null;
  er_blocking_top_k?: number | null;
  confidence_threshold?: number | null;
  max_reflection_attempts?: number | null;
  max_cypher_healing_attempts?: number | null;
  max_hallucination_retries?: number | null;
  enable_schema_enrichment?: boolean | null;
  enable_cypher_healing?: boolean | null;
  enable_critic_validation?: boolean | null;
  enable_hallucination_grader?: boolean | null;
  enable_retrieval_quality_gate?: boolean | null;
  enable_grader_consistency_validator?: boolean | null;
  enable_spacy_heuristics?: boolean | null;
  enable_lazy_expansion?: boolean | null;
}

// ── Demo API Models ─────────────────────────────────────────────────────────
export interface BuildRequest {
  doc_paths: string[];
  ddl_paths: string[];
  clear_graph?: boolean;
  study_id?: string;
  lazy_extraction?: boolean;
  config?: PipelineConfig | null;
}

export type JobStatus = "queued" | "running" | "done" | "failed";

export interface BuildResultResponse {
  job_id: string;
  status: JobStatus;
  error?: string | null;
  triplets_extracted?: number | null;
  entities_resolved?: number | null;
  tables_parsed?: number | null;
  tables_completed?: number | null;
  parent_chunks?: number | null;
  child_chunks?: number | null;
  current_step?: string | null;
}

export interface QueryRequest {
  question: string;
  config?: PipelineConfig | null;
}

export interface QueryResponse {
  answer: string;
  sources: string[];
  retrieval_quality_score: number;
  retrieval_chunk_count: number;
  gate_decision: string;
  grounded: boolean;
  context_previews: string[];
}

export interface PipelineRequest {
  doc_paths: string[];
  ddl_paths: string[];
  questions: string[];
  clear_graph?: boolean;
  lazy_extraction?: boolean;
  run_ragas?: boolean;
  study_id?: string;
  config?: PipelineConfig | null;
}

export interface PipelineJobResponse {
  job_id: string;
  status: JobStatus;
  num_questions: number;
}

export interface PipelineResultResponse {
  job_id: string;
  status: JobStatus;
  error?: string | null;
  builder?: BuildResultResponse | null;
  answers?: QueryResponse[] | null;
  ragas?: Record<string, number> | null;
}

export interface GraphStatsResponse {
  business_concepts: number;
  physical_tables: number;
  parent_chunks: number;
  child_chunks: number;
  mentions_edges: number;
  maps_to_edges: number;
  child_of_edges: number;
  references_edges: number;
  total_nodes: number;
  total_relationships: number;
}

export interface GraphNodeData {
  id: string;
  label: string;
  group: string;
  confidence?: number | null;
  properties?: Record<string, unknown>;
}

export interface GraphEdgeData {
  id: string;
  from: string;
  to: string;
  label: string;
  confidence?: number | null;
}

export interface GraphDataResponse {
  nodes: GraphNodeData[];
  edges: GraphEdgeData[];
}

export interface DemoJob {
  job_id: string;
  type: string;
  status: JobStatus;
  study_id: string;
  num_questions?: number | null;
}

// ── Ablation API Models ─────────────────────────────────────────────────────
export interface CustomAblationRequest {
  dataset?: string;
  study_id?: string;
  max_samples?: number | null;
  run_ragas?: boolean;
  ragas_model?: string;
  skip_builder?: boolean;
  lazy_extraction?: boolean;
  retrieval_mode?: RetrievalMode | null;
  enable_reranker?: boolean | null;
  reranker_top_k?: number | null;
  enable_hallucination_grader?: boolean | null;
  enable_cypher_healing?: boolean | null;
  enable_critic_validation?: boolean | null;
  enable_schema_enrichment?: boolean | null;
  chunk_size?: number | null;
  chunk_overlap?: number | null;
  parent_chunk_size?: number | null;
  er_similarity_threshold?: number | null;
  er_blocking_top_k?: number | null;
  confidence_threshold?: number | null;
  retrieval_vector_top_k?: number | null;
  llm_max_tokens_extraction?: number | null;
  reasoning_model?: string | null;
  extraction_model?: string | null;
  provider_base_url?: string | null;
}

export interface PresetAblationRequest {
  study_id: string;
  dataset?: string;
  max_samples?: number | null;
  run_ragas?: boolean;
  ragas_model?: string;
  skip_builder?: boolean;
  reasoning_model?: string | null;
  extraction_model?: string | null;
  provider_base_url?: string | null;
}

export interface AblationJobResponse {
  job_id: string;
  status: JobStatus;
  study_id: string;
  dataset: string;
}

export interface PresetAblationJobResponse extends AblationJobResponse {
  description: string;
  applied_env_overrides: Record<string, string>;
}

export interface AblationResultResponse {
  job_id: string;
  status: JobStatus;
  study_id: string;
  error?: string | null;
  summary?: Record<string, unknown> | null;
  ragas?: Record<string, number> | null;
  per_question?: Record<string, unknown>[] | null;
  bundle_path?: string | null;
}

export interface AblationMatrixEntry {
  study_id: string;
  description: string;
  env_overrides: Record<string, string>;
  run_ragas: boolean;
}

// ── Health ──────────────────────────────────────────────────────────────────
export interface HealthResponse {
  status: string;
}

// ── AI Judge ────────────────────────────────────────────────────────────────
export interface AIJudgePayload {
  system_prompt: string;
  evaluation_bundle: Record<string, unknown>;
  instructions: string;
}
