import {
  createContext,
  useContext,
  useState,
  useCallback,
  type ReactNode,
} from "react";

import type { PipelineConfig, LLMProvider } from "@/types/api";

// ── Persisted settings shape ──────────────────────────────────────────────

export interface PersistedSettings {
  // ── Frontend connection ─────────────────────────────────────────────────
  apiKey: string;
  apiBaseUrl: string;

  // ── LLM Provider & API Keys ────────────────────────────────────────────
  llm_provider: LLMProvider | "auto";
  lmstudio_base_url: string;
  openrouter_api_key: string;
  openai_api_key: string;
  anthropic_api_key: string;
  groq_api_key: string;
  mistral_api_key: string;

  // ── LLM Models ─────────────────────────────────────────────────────────
  llm_model_reasoning: string;
  llm_model_extraction: string;
  llm_model_midtier: string;
  temperature_extraction: number;
  temperature_reasoning: number;
  temperature_generation: number;
  max_tokens_extraction: number;
  max_tokens_reasoning: number;

  // ── Chunking ───────────────────────────────────────────────────────────
  chunk_size: number;
  chunk_overlap: number;
  parent_chunk_size: number;
  parent_chunk_overlap: number;

  // ── Entity Resolution ──────────────────────────────────────────────────
  er_blocking_top_k: number;
  er_similarity_threshold: number;

  // ── Retrieval ──────────────────────────────────────────────────────────
  retrieval_mode: "hybrid" | "vector" | "bm25";
  retrieval_vector_top_k: number;
  retrieval_bm25_top_k: number;
  reranker_top_k: number;
  confidence_threshold: number;

  // ── Loop Guards ────────────────────────────────────────────────────────
  max_reflection_attempts: number;
  max_cypher_healing_attempts: number;
  max_hallucination_retries: number;

  // ── Performance / Cost Optimisation ───────────────────────────────────
  enable_singleton_llm_definitions: boolean;
  critic_confidence_gate: number;
  max_reflection_attempts_reasoning: number;

  // ── Feature Flags ──────────────────────────────────────────────────────
  enable_schema_enrichment: boolean;
  enable_cypher_healing: boolean;
  enable_critic_validation: boolean;
  enable_hallucination_grader: boolean;
  enable_reranker: boolean;
  enable_retrieval_quality_gate: boolean;
  enable_grader_consistency_validator: boolean;
  enable_spacy_heuristics: boolean;
  enable_lazy_expansion: boolean;
  use_lazy_extraction: boolean;

  // ── Debug ──────────────────────────────────────────────────────────────
  log_level: "DEBUG" | "INFO" | "WARNING" | "ERROR";
  enable_debug_trace: boolean;
}

export const DEFAULT_SETTINGS: PersistedSettings = {
  apiKey: "",
  apiBaseUrl: "/api/v1",
  llm_provider: "auto",
  lmstudio_base_url: "http://localhost:1234/v1",
  openrouter_api_key: "",
  openai_api_key: "",
  anthropic_api_key: "",
  groq_api_key: "",
  mistral_api_key: "",
  llm_model_reasoning: "openai/gpt-oss-120b",
  llm_model_extraction: "openai/gpt-4.1-nano",
  llm_model_midtier: "openai/gpt-4.1-nano",
  temperature_extraction: 0.0,
  temperature_reasoning: 0.0,
  temperature_generation: 0.3,
  max_tokens_extraction: 8192,
  max_tokens_reasoning: 4096,
  chunk_size: 256,
  chunk_overlap: 32,
  parent_chunk_size: 800,
  parent_chunk_overlap: 96,
  er_blocking_top_k: 10,
  er_similarity_threshold: 0.75,
  retrieval_mode: "hybrid",
  retrieval_vector_top_k: 20,
  retrieval_bm25_top_k: 10,
  reranker_top_k: 12,
  confidence_threshold: 0.90,
  max_reflection_attempts: 3,
  max_cypher_healing_attempts: 3,
  max_hallucination_retries: 3,
  enable_singleton_llm_definitions: false,
  critic_confidence_gate: 0.85,
  max_reflection_attempts_reasoning: 2,
  enable_schema_enrichment: true,
  enable_cypher_healing: true,
  enable_critic_validation: true,
  enable_hallucination_grader: true,
  enable_reranker: true,
  enable_retrieval_quality_gate: true,
  enable_grader_consistency_validator: true,
  enable_spacy_heuristics: true,
  enable_lazy_expansion: true,
  use_lazy_extraction: false,
  log_level: "INFO",
  enable_debug_trace: false,
};

const LS_KEY = "thesis_settings_v2";

function loadFromStorage(): PersistedSettings {
  try {
    const raw = localStorage.getItem(LS_KEY);
    if (raw) return { ...DEFAULT_SETTINGS, ...JSON.parse(raw) };
  } catch { /* ignore */ }
  // Legacy keys
  return {
    ...DEFAULT_SETTINGS,
    apiKey: localStorage.getItem("thesis_api_key") || "",
    apiBaseUrl: localStorage.getItem("thesis_api_base_url") || "/api/v1",
  };
}

// ── Context shape ─────────────────────────────────────────────────────────

interface SettingsState {
  settings: PersistedSettings;
  updateSetting: <K extends keyof PersistedSettings>(key: K, value: PersistedSettings[K]) => void;
  updateSettings: (patch: Partial<PersistedSettings>) => void;
  resetToDefaults: () => void;
  saveToLocalStorage: () => void;
  applyToServer: () => Promise<{ applied: string[]; masked: string[] }>;
  getGlobalPipelineConfig: () => PipelineConfig;
  // Legacy compat
  apiKey: string;
  apiBaseUrl: string;
  setApiKey: (key: string) => void;
  setApiBaseUrl: (url: string) => void;
}

const SettingsContext = createContext<SettingsState | null>(null);

// ── Provider ──────────────────────────────────────────────────────────────

export function SettingsProvider({ children }: { children: ReactNode }) {
  const [settings, setSettings] = useState<PersistedSettings>(loadFromStorage);

  const persist = (next: PersistedSettings) => {
    localStorage.setItem(LS_KEY, JSON.stringify(next));
    if (next.apiKey) localStorage.setItem("thesis_api_key", next.apiKey);
    else localStorage.removeItem("thesis_api_key");
    localStorage.setItem("thesis_api_base_url", next.apiBaseUrl);
  };

  const updateSetting = useCallback(
    <K extends keyof PersistedSettings>(key: K, value: PersistedSettings[K]) => {
      setSettings((prev) => {
        const next = { ...prev, [key]: value };
        persist(next);
        return next;
      });
    },
    [],
  );

  const updateSettings = useCallback((patch: Partial<PersistedSettings>) => {
    setSettings((prev) => {
      const next = { ...prev, ...patch };
      persist(next);
      return next;
    });
  }, []);

  const resetToDefaults = useCallback(() => {
    const next = { ...DEFAULT_SETTINGS };
    persist(next);
    setSettings(next);
  }, []);

  const saveToLocalStorage = useCallback(() => persist(settings), [settings]);

  const applyToServer = useCallback(async () => {
    const s = settings;
    const overrides: Record<string, string> = {
      LLM_PROVIDER: s.llm_provider,
      LMSTUDIO_BASE_URL: s.lmstudio_base_url,
      LLM_MODEL_REASONING: s.llm_model_reasoning,
      LLM_MODEL_EXTRACTION: s.llm_model_extraction,
      LLM_MODEL_MIDTIER: s.llm_model_midtier,
      LLM_TEMPERATURE_EXTRACTION: String(s.temperature_extraction),
      LLM_TEMPERATURE_REASONING: String(s.temperature_reasoning),
      LLM_TEMPERATURE_GENERATION: String(s.temperature_generation),
      LLM_MAX_TOKENS_EXTRACTION: String(s.max_tokens_extraction),
      LLM_MAX_TOKENS_REASONING: String(s.max_tokens_reasoning),
      CHUNK_SIZE: String(s.chunk_size),
      CHUNK_OVERLAP: String(s.chunk_overlap),
      PARENT_CHUNK_SIZE: String(s.parent_chunk_size),
      PARENT_CHUNK_OVERLAP: String(s.parent_chunk_overlap),
      ER_BLOCKING_TOP_K: String(s.er_blocking_top_k),
      ER_SIMILARITY_THRESHOLD: String(s.er_similarity_threshold),
      RETRIEVAL_MODE: s.retrieval_mode,
      RETRIEVAL_VECTOR_TOP_K: String(s.retrieval_vector_top_k),
      RETRIEVAL_BM25_TOP_K: String(s.retrieval_bm25_top_k),
      RERANKER_TOP_K: String(s.reranker_top_k),
      CONFIDENCE_THRESHOLD: String(s.confidence_threshold),
      MAX_REFLECTION_ATTEMPTS: String(s.max_reflection_attempts),
      MAX_CYPHER_HEALING_ATTEMPTS: String(s.max_cypher_healing_attempts),
      MAX_HALLUCINATION_RETRIES: String(s.max_hallucination_retries),
      ENABLE_SINGLETON_LLM_DEFINITIONS: s.enable_singleton_llm_definitions ? "true" : "false",
      CRITIC_CONFIDENCE_GATE: String(s.critic_confidence_gate),
      MAX_REFLECTION_ATTEMPTS_REASONING: String(s.max_reflection_attempts_reasoning),
      ENABLE_SCHEMA_ENRICHMENT: s.enable_schema_enrichment ? "true" : "false",
      ENABLE_CYPHER_HEALING: s.enable_cypher_healing ? "true" : "false",
      ENABLE_CRITIC_VALIDATION: s.enable_critic_validation ? "true" : "false",
      ENABLE_HALLUCINATION_GRADER: s.enable_hallucination_grader ? "true" : "false",
      ENABLE_RERANKER: s.enable_reranker ? "true" : "false",
      ENABLE_RETRIEVAL_QUALITY_GATE: s.enable_retrieval_quality_gate ? "true" : "false",
      ENABLE_GRADER_CONSISTENCY_VALIDATOR: s.enable_grader_consistency_validator ? "true" : "false",
      ENABLE_SPACY_HEURISTICS: s.enable_spacy_heuristics ? "true" : "false",
      ENABLE_LAZY_EXPANSION: s.enable_lazy_expansion ? "true" : "false",
      USE_LAZY_EXTRACTION: s.use_lazy_extraction ? "true" : "false",
      LOG_LEVEL: s.log_level,
      ENABLE_DEBUG_TRACE: s.enable_debug_trace ? "true" : "false",
    };
    if (s.openrouter_api_key) overrides["OPENROUTER_API_KEY"] = s.openrouter_api_key;
    if (s.openai_api_key) overrides["OPENAI_API_KEY"] = s.openai_api_key;
    if (s.anthropic_api_key) overrides["ANTHROPIC_API_KEY"] = s.anthropic_api_key;
    if (s.groq_api_key) overrides["GROQ_API_KEY"] = s.groq_api_key;
    if (s.mistral_api_key) overrides["MISTRAL_API_KEY"] = s.mistral_api_key;

    const baseUrl = s.apiBaseUrl || "/api/v1";
    const headers: Record<string, string> = { "Content-Type": "application/json" };
    if (s.apiKey) headers["X-API-Key"] = s.apiKey;

    const res = await fetch(`${baseUrl}/config`, {
      method: "POST",
      headers,
      body: JSON.stringify({ overrides }),
    });
    if (!res.ok) {
      const errTxt = await res.text();
      throw new Error(`Config apply failed: ${res.status} ${errTxt}`);
    }
    return res.json() as Promise<{ applied: string[]; masked: string[] }>;
  }, [settings]);

  const getGlobalPipelineConfig = useCallback((): PipelineConfig => {
    const s = settings;
    return {
      provider: s.llm_provider === "auto" ? null : (s.llm_provider as LLMProvider),
      reasoning_model: s.llm_model_reasoning || null,
      extraction_model: s.llm_model_extraction || null,
      midtier_model: s.llm_model_midtier || null,
      lmstudio_base_url: s.lmstudio_base_url || null,
      temperature_extraction: s.temperature_extraction,
      temperature_reasoning: s.temperature_reasoning,
      temperature_generation: s.temperature_generation,
      max_tokens_extraction: s.max_tokens_extraction,
      max_tokens_reasoning: s.max_tokens_reasoning,
      chunk_size: s.chunk_size,
      chunk_overlap: s.chunk_overlap,
      parent_chunk_size: s.parent_chunk_size,
      parent_chunk_overlap: s.parent_chunk_overlap,
      retrieval_mode: s.retrieval_mode,
      retrieval_vector_top_k: s.retrieval_vector_top_k,
      retrieval_bm25_top_k: s.retrieval_bm25_top_k,
      enable_reranker: s.enable_reranker,
      reranker_top_k: s.reranker_top_k,
      er_similarity_threshold: s.er_similarity_threshold,
      er_blocking_top_k: s.er_blocking_top_k,
      confidence_threshold: s.confidence_threshold,
      max_reflection_attempts: s.max_reflection_attempts,
      max_cypher_healing_attempts: s.max_cypher_healing_attempts,
      max_hallucination_retries: s.max_hallucination_retries,
      enable_schema_enrichment: s.enable_schema_enrichment,
      enable_cypher_healing: s.enable_cypher_healing,
      enable_critic_validation: s.enable_critic_validation,
      enable_hallucination_grader: s.enable_hallucination_grader,
      enable_retrieval_quality_gate: s.enable_retrieval_quality_gate,
      enable_grader_consistency_validator: s.enable_grader_consistency_validator,
      enable_spacy_heuristics: s.enable_spacy_heuristics,
      enable_lazy_expansion: s.enable_lazy_expansion,
    };
  }, [settings]);

  const setApiKey = useCallback((k: string) => updateSetting("apiKey", k), [updateSetting]);
  const setApiBaseUrl = useCallback((u: string) => updateSetting("apiBaseUrl", u), [updateSetting]);

  return (
    <SettingsContext.Provider
      value={{
        settings,
        updateSetting,
        updateSettings,
        resetToDefaults,
        saveToLocalStorage,
        applyToServer,
        getGlobalPipelineConfig,
        apiKey: settings.apiKey,
        apiBaseUrl: settings.apiBaseUrl,
        setApiKey,
        setApiBaseUrl,
      }}
    >
      {children}
    </SettingsContext.Provider>
  );
}

export function useSettings(): SettingsState {
  const ctx = useContext(SettingsContext);
  if (!ctx) throw new Error("useSettings must be used within SettingsProvider");
  return ctx;
}
