import { useState } from "react";
import {
  Save,
  RotateCcw,
  Wifi,
  WifiOff,
  Cpu,
  KeyRound,
  Sliders,
  ToggleLeft,
  Moon,
  CheckCircle2,
  Loader2,
  Server,
  Bug,
} from "lucide-react";
import {
  Card,
  CardContent,
  CardDescription,
  CardTitle,
} from "@/components/ui/card";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import { Separator } from "@/components/ui/separator";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { useSettings } from "@/contexts/SettingsContext";
import { useHealth } from "@/hooks/useJobs";
import { toast } from "sonner";

// ── Helper components ────────────────────────────────────────────────────────

function SettingRow({
  label,
  description,
  children,
}: {
  label: string;
  description?: string;
  children: React.ReactNode;
}) {
  return (
    <div className="grid grid-cols-3 gap-4 items-center py-2">
      <div>
        <p className="text-sm font-medium">{label}</p>
        {description && <p className="text-xs text-muted-foreground">{description}</p>}
      </div>
      <div className="col-span-2">{children}</div>
    </div>
  );
}

function FlagRow({
  id,
  label,
  description,
  checked,
  onCheckedChange,
}: {
  id: string;
  label: string;
  description?: string;
  checked: boolean;
  onCheckedChange: (v: boolean) => void;
}) {
  return (
    <div className="flex items-start gap-3 py-1.5">
      <Switch id={id} checked={checked} onCheckedChange={onCheckedChange} className="mt-0.5" />
      <div>
        <Label htmlFor={id} className="text-sm cursor-pointer">{label}</Label>
        {description && <p className="text-xs text-muted-foreground">{description}</p>}
      </div>
    </div>
  );
}

export function SettingsPage() {
  const { settings, updateSetting, resetToDefaults, applyToServer } = useSettings();
  const { data: health } = useHealth();
  const [connectionTesting, setConnectionTesting] = useState(false);
  const [applying, setApplying] = useState(false);

  const systemOk = health?.status === "ok" || health?.status === "healthy";

  const upd = <K extends keyof typeof settings>(key: K) =>
    (val: (typeof settings)[K]) => updateSetting(key, val);

  const handleTestConnection = async () => {
    setConnectionTesting(true);
    try {
      const res = await fetch(settings.apiBaseUrl.replace(/\/api\/v1\/?$/, "") + "/health");
      const data = await res.json();
      if (data.status === "ok" || data.status === "healthy") {
        toast.success("Connection successful", { description: "API is reachable and healthy." });
      } else {
        toast.warning("Connection unstable", { description: `API returned status: ${data.status}` });
      }
    } catch {
      toast.error("Connection failed", { description: "Could not reach the API server." });
    } finally {
      setConnectionTesting(false);
    }
  };

  const handleApplyToServer = async () => {
    setApplying(true);
    try {
      const result = await applyToServer();
      toast.success("Settings applied to server", {
        description: `${result.applied.length} env vars updated.`,
      });
    } catch (err) {
      toast.error("Failed to apply settings", {
        description: err instanceof Error ? err.message : "Unknown error",
      });
    } finally {
      setApplying(false);
    }
  };

  const handleReset = () => {
    resetToDefaults();
    toast.info("Settings reset to defaults");
  };

  return (
    <div className="p-6 space-y-6 max-w-4xl">
      <div>
        <h1 className="text-2xl font-bold tracking-tight">Settings</h1>
        <p className="text-sm text-muted-foreground">
          Configure the GraphRAG Studio backend, LLM providers, and pipeline parameters.
          Changes are saved locally immediately; use <strong>Apply to Server</strong> to push them to the running backend.
        </p>
      </div>

      <div className="flex gap-3">
        <Button onClick={handleApplyToServer} disabled={applying}>
          {applying ? <Loader2 className="mr-2 size-4 animate-spin" /> : <Server className="mr-2 size-4" />}
          Apply to Server
        </Button>
        <Button variant="outline" onClick={handleReset}>
          <RotateCcw className="mr-2 size-4" />
          Reset to Defaults
        </Button>
      </div>

      <Accordion type="multiple" defaultValue={["connection", "llm-keys"]} className="space-y-4">

        {/* 1. API Connection */}
        <AccordionItem value="connection" className="border rounded-lg">
          <AccordionTrigger className="px-6 py-4 hover:no-underline">
            <CardTitle className="flex items-center gap-2 text-base">
              {systemOk ? <Wifi className="size-4 text-emerald-400" /> : <WifiOff className="size-4 text-red-400" />}
              API Connection
            </CardTitle>
          </AccordionTrigger>
          <AccordionContent>
            <CardContent className="pt-0 space-y-4">
              <CardDescription>Configure the backend endpoint and frontend authentication header.</CardDescription>
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="api-base-url">Base URL</Label>
                  <Input id="api-base-url" value={settings.apiBaseUrl} onChange={(e) => upd("apiBaseUrl")(e.target.value)} placeholder="http://localhost:8000/api/v1" />
                  <p className="text-xs text-muted-foreground">VITE_API_BASE_URL or Vite proxy</p>
                </div>
                <div className="space-y-2">
                  <Label htmlFor="api-key">API Key</Label>
                  <Input id="api-key" type="password" value={settings.apiKey} onChange={(e) => upd("apiKey")(e.target.value)} placeholder="Optional X-API-Key header" />
                  <p className="text-xs text-muted-foreground">Leave empty if auth is off</p>
                </div>
              </div>
              <div className="flex items-center gap-3">
                <Button variant="outline" onClick={handleTestConnection} disabled={connectionTesting}>
                  {connectionTesting ? <Loader2 className="mr-2 size-4 animate-spin" /> : systemOk ? <CheckCircle2 className="mr-2 size-4 text-emerald-400" /> : <Wifi className="mr-2 size-4" />}
                  Test Connection
                </Button>
                {health && <span className={`text-sm ${systemOk ? "text-emerald-400" : "text-red-400"}`}>{systemOk ? "Connected" : "Disconnected"}</span>}
              </div>
            </CardContent>
          </AccordionContent>
        </AccordionItem>

        {/* 2. LLM Providers & API Keys */}
        <AccordionItem value="llm-keys" className="border rounded-lg">
          <AccordionTrigger className="px-6 py-4 hover:no-underline">
            <CardTitle className="flex items-center gap-2 text-base"><KeyRound className="size-4" />LLM Providers &amp; API Keys</CardTitle>
          </AccordionTrigger>
          <AccordionContent>
            <CardContent className="pt-0 space-y-1 divide-y divide-border">
              <CardDescription className="pb-3">Select your provider and supply API keys. Keys are stored in localStorage and sent to the server via Apply to Server.</CardDescription>
              <SettingRow label="Provider" description="Active LLM routing backend">
                <Select value={settings.llm_provider} onValueChange={upd("llm_provider") as (v: string) => void}>
                  <SelectTrigger><SelectValue /></SelectTrigger>
                  <SelectContent>
                    {["auto","openrouter","openai","anthropic","lmstudio","ollama","groq","mistral","google","together","deepseek","xai"].map(p => (
                      <SelectItem key={p} value={p}>{p}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </SettingRow>
              <SettingRow label="LMStudio Base URL" description="Local LMStudio server endpoint">
                <Input value={settings.lmstudio_base_url} onChange={(e) => upd("lmstudio_base_url")(e.target.value)} placeholder="http://localhost:1234/v1" />
              </SettingRow>
              <SettingRow label="OpenRouter API Key" description="OPENROUTER_API_KEY">
                <Input type="password" value={settings.openrouter_api_key} onChange={(e) => upd("openrouter_api_key")(e.target.value)} placeholder="sk-or-..." />
              </SettingRow>
              <SettingRow label="OpenAI API Key" description="OPENAI_API_KEY">
                <Input type="password" value={settings.openai_api_key} onChange={(e) => upd("openai_api_key")(e.target.value)} placeholder="sk-..." />
              </SettingRow>
              <SettingRow label="Anthropic API Key" description="ANTHROPIC_API_KEY">
                <Input type="password" value={settings.anthropic_api_key} onChange={(e) => upd("anthropic_api_key")(e.target.value)} placeholder="sk-ant-..." />
              </SettingRow>
              <SettingRow label="Groq API Key" description="GROQ_API_KEY">
                <Input type="password" value={settings.groq_api_key} onChange={(e) => upd("groq_api_key")(e.target.value)} placeholder="gsk_..." />
              </SettingRow>
              <SettingRow label="Mistral API Key" description="MISTRAL_API_KEY">
                <Input type="password" value={settings.mistral_api_key} onChange={(e) => upd("mistral_api_key")(e.target.value)} placeholder="..." />
              </SettingRow>
            </CardContent>
          </AccordionContent>
        </AccordionItem>

        {/* 3. LLM Models & Parameters */}
        <AccordionItem value="llm-models" className="border rounded-lg">
          <AccordionTrigger className="px-6 py-4 hover:no-underline">
            <CardTitle className="flex items-center gap-2 text-base"><Cpu className="size-4" />LLM Models &amp; Parameters</CardTitle>
          </AccordionTrigger>
          <AccordionContent>
            <CardContent className="pt-0 space-y-1 divide-y divide-border">
              <SettingRow label="Reasoning Model" description="Main RAG generation and reasoning">
                <Input value={settings.llm_model_reasoning} onChange={(e) => upd("llm_model_reasoning")(e.target.value)} placeholder="openai/gpt-oss-120b" />
              </SettingRow>
              <SettingRow label="Extraction Model" description="Structured JSON extraction">
                <Input value={settings.llm_model_extraction} onChange={(e) => upd("llm_model_extraction")(e.target.value)} placeholder="openai/gpt-4.1-nano" />
              </SettingRow>
              <SettingRow label="Midtier Model" description="Mapping, Actor-Critic, grading">
                <Input value={settings.llm_model_midtier} onChange={(e) => upd("llm_model_midtier")(e.target.value)} placeholder="openai/gpt-4.1-nano" />
              </SettingRow>
              <Separator className="my-2" />
              <SettingRow label="Temperature — Extraction" description="0.0 = deterministic JSON">
                <Input type="number" step="0.1" min="0" max="2" value={settings.temperature_extraction} onChange={(e) => upd("temperature_extraction")(parseFloat(e.target.value))} />
              </SettingRow>
              <SettingRow label="Temperature — Reasoning" description="0.0 = deterministic">
                <Input type="number" step="0.1" min="0" max="2" value={settings.temperature_reasoning} onChange={(e) => upd("temperature_reasoning")(parseFloat(e.target.value))} />
              </SettingRow>
              <SettingRow label="Temperature — Generation" description="0.3 for fluency">
                <Input type="number" step="0.1" min="0" max="2" value={settings.temperature_generation} onChange={(e) => upd("temperature_generation")(parseFloat(e.target.value))} />
              </SettingRow>
              <SettingRow label="Max Tokens — Extraction" description="Max output tokens for extraction LLM">
                <Input type="number" step="512" min="256" value={settings.max_tokens_extraction} onChange={(e) => upd("max_tokens_extraction")(parseInt(e.target.value))} />
              </SettingRow>
              <SettingRow label="Max Tokens — Reasoning" description="Max output tokens for reasoning LLM">
                <Input type="number" step="512" min="256" value={settings.max_tokens_reasoning} onChange={(e) => upd("max_tokens_reasoning")(parseInt(e.target.value))} />
              </SettingRow>
            </CardContent>
          </AccordionContent>
        </AccordionItem>

        {/* 4. Chunking */}
        <AccordionItem value="chunking" className="border rounded-lg">
          <AccordionTrigger className="px-6 py-4 hover:no-underline">
            <CardTitle className="flex items-center gap-2 text-base"><Sliders className="size-4" />Chunking</CardTitle>
          </AccordionTrigger>
          <AccordionContent>
            <CardContent className="pt-0 space-y-1 divide-y divide-border">
              <SettingRow label="Child Chunk Size" description="Tokens per child chunk">
                <Input type="number" step="32" min="64" value={settings.chunk_size} onChange={(e) => upd("chunk_size")(parseInt(e.target.value))} />
              </SettingRow>
              <SettingRow label="Child Chunk Overlap" description="Overlap tokens between children">
                <Input type="number" step="8" min="0" value={settings.chunk_overlap} onChange={(e) => upd("chunk_overlap")(parseInt(e.target.value))} />
              </SettingRow>
              <SettingRow label="Parent Chunk Size" description="Tokens per parent context chunk">
                <Input type="number" step="64" min="128" value={settings.parent_chunk_size} onChange={(e) => upd("parent_chunk_size")(parseInt(e.target.value))} />
              </SettingRow>
              <SettingRow label="Parent Chunk Overlap" description="Overlap tokens between parents">
                <Input type="number" step="16" min="0" value={settings.parent_chunk_overlap} onChange={(e) => upd("parent_chunk_overlap")(parseInt(e.target.value))} />
              </SettingRow>
            </CardContent>
          </AccordionContent>
        </AccordionItem>

        {/* 5. Entity Resolution & Retrieval */}
        <AccordionItem value="er-retrieval" className="border rounded-lg">
          <AccordionTrigger className="px-6 py-4 hover:no-underline">
            <CardTitle className="flex items-center gap-2 text-base"><Sliders className="size-4" />Entity Resolution &amp; Retrieval</CardTitle>
          </AccordionTrigger>
          <AccordionContent>
            <CardContent className="pt-0 space-y-1 divide-y divide-border">
              <SettingRow label="ER Blocking Top-K" description="Candidates per entity for blocking">
                <Input type="number" step="1" min="1" value={settings.er_blocking_top_k} onChange={(e) => upd("er_blocking_top_k")(parseInt(e.target.value))} />
              </SettingRow>
              <SettingRow label="ER Similarity Threshold" description="Min cosine similarity for merging">
                <Input type="number" step="0.05" min="0" max="1" value={settings.er_similarity_threshold} onChange={(e) => upd("er_similarity_threshold")(parseFloat(e.target.value))} />
              </SettingRow>
              <Separator className="my-2" />
              <SettingRow label="Retrieval Mode" description="Channel combination strategy">
                <Select value={settings.retrieval_mode} onValueChange={upd("retrieval_mode") as (v: string) => void}>
                  <SelectTrigger><SelectValue /></SelectTrigger>
                  <SelectContent>
                    <SelectItem value="hybrid">hybrid</SelectItem>
                    <SelectItem value="vector">vector</SelectItem>
                    <SelectItem value="bm25">bm25</SelectItem>
                  </SelectContent>
                </Select>
              </SettingRow>
              <SettingRow label="Vector Top-K" description="Dense retrieval candidates">
                <Input type="number" step="1" min="1" value={settings.retrieval_vector_top_k} onChange={(e) => upd("retrieval_vector_top_k")(parseInt(e.target.value))} />
              </SettingRow>
              <SettingRow label="BM25 Top-K" description="Sparse retrieval candidates">
                <Input type="number" step="1" min="1" value={settings.retrieval_bm25_top_k} onChange={(e) => upd("retrieval_bm25_top_k")(parseInt(e.target.value))} />
              </SettingRow>
              <SettingRow label="Reranker Top-K" description="Passages passed to LLM after reranking">
                <Input type="number" step="1" min="1" value={settings.reranker_top_k} onChange={(e) => upd("reranker_top_k")(parseInt(e.target.value))} />
              </SettingRow>
              <SettingRow label="Confidence Threshold" description="Mapping confidence for HITL gate">
                <Input type="number" step="0.05" min="0" max="1" value={settings.confidence_threshold} onChange={(e) => upd("confidence_threshold")(parseFloat(e.target.value))} />
              </SettingRow>
            </CardContent>
          </AccordionContent>
        </AccordionItem>

        {/* 6. Feature Flags */}
        <AccordionItem value="feature-flags" className="border rounded-lg">
          <AccordionTrigger className="px-6 py-4 hover:no-underline">
            <CardTitle className="flex items-center gap-2 text-base"><ToggleLeft className="size-4" />Feature Flags</CardTitle>
          </AccordionTrigger>
          <AccordionContent>
            <CardContent className="pt-0">
              <CardDescription className="mb-4">Enable or disable pipeline components. Useful for ablation experiments.</CardDescription>
              <div className="grid grid-cols-2 gap-x-8 gap-y-1">
                <FlagRow id="f-schema" label="Schema Enrichment" description="LLM acronym expansion during schema build" checked={settings.enable_schema_enrichment} onCheckedChange={upd("enable_schema_enrichment")} />
                <FlagRow id="f-cypher" label="Cypher Healing" description="Auto-fix Cypher syntax errors via LLM" checked={settings.enable_cypher_healing} onCheckedChange={upd("enable_cypher_healing")} />
                <FlagRow id="f-critic" label="Critic Validation" description="Actor-Critic mapping validation loop" checked={settings.enable_critic_validation} onCheckedChange={upd("enable_critic_validation")} />
                <FlagRow id="f-halluc" label="Hallucination Grader" description="Self-RAG hallucination grading" checked={settings.enable_hallucination_grader} onCheckedChange={upd("enable_hallucination_grader")} />
                <FlagRow id="f-reranker" label="Reranker" description="Cross-encoder reranking (bge-reranker-v2-m3)" checked={settings.enable_reranker} onCheckedChange={upd("enable_reranker")} />
                <FlagRow id="f-qgate" label="Retrieval Quality Gate" description="Gate before generation" checked={settings.enable_retrieval_quality_gate} onCheckedChange={upd("enable_retrieval_quality_gate")} />
                <FlagRow id="f-gconsist" label="Grader Consistency" description="Grader consistency across iterations" checked={settings.enable_grader_consistency_validator} onCheckedChange={upd("enable_grader_consistency_validator")} />
                <FlagRow id="f-spacy" label="spaCy Heuristics" description="spaCy-based extraction fallback" checked={settings.enable_spacy_heuristics} onCheckedChange={upd("enable_spacy_heuristics")} />
                <FlagRow id="f-lazy-exp" label="Lazy Expansion" description="Lazy context expansion strategy" checked={settings.enable_lazy_expansion} onCheckedChange={upd("enable_lazy_expansion")} />
                <FlagRow id="f-lazy-ext" label="Lazy Extraction" description="Rule-based extraction instead of LLM" checked={settings.use_lazy_extraction} onCheckedChange={upd("use_lazy_extraction")} />
              </div>
            </CardContent>
          </AccordionContent>
        </AccordionItem>

        {/* 7. Performance & Loop Guards */}
        <AccordionItem value="perf-guards" className="border rounded-lg">
          <AccordionTrigger className="px-6 py-4 hover:no-underline">
            <CardTitle className="flex items-center gap-2 text-base"><Save className="size-4" />Performance &amp; Loop Guards</CardTitle>
          </AccordionTrigger>
          <AccordionContent>
            <CardContent className="pt-0 space-y-1 divide-y divide-border">
              <div className="py-2">
                <FlagRow id="f-singleton" label="Singleton LLM Definitions" description="Re-use LLM client instances across calls" checked={settings.enable_singleton_llm_definitions} onCheckedChange={upd("enable_singleton_llm_definitions")} />
              </div>
              <SettingRow label="Critic Confidence Gate" description="Min score below which critic skips">
                <Input type="number" step="0.05" min="0" max="1" value={settings.critic_confidence_gate} onChange={(e) => upd("critic_confidence_gate")(parseFloat(e.target.value))} />
              </SettingRow>
              <SettingRow label="Max Reflection Attempts (Reasoning)" description="Reflection loop limit for RAG graph">
                <Input type="number" step="1" min="0" value={settings.max_reflection_attempts_reasoning} onChange={(e) => upd("max_reflection_attempts_reasoning")(parseInt(e.target.value))} />
              </SettingRow>
              <SettingRow label="Max Reflection Attempts" description="Actor-Critic reflection retries">
                <Input type="number" step="1" min="0" value={settings.max_reflection_attempts} onChange={(e) => upd("max_reflection_attempts")(parseInt(e.target.value))} />
              </SettingRow>
              <SettingRow label="Max Cypher Healing Attempts" description="Cypher healing retries before fallback">
                <Input type="number" step="1" min="0" value={settings.max_cypher_healing_attempts} onChange={(e) => upd("max_cypher_healing_attempts")(parseInt(e.target.value))} />
              </SettingRow>
              <SettingRow label="Max Hallucination Retries" description="Hallucination grader retry budget">
                <Input type="number" step="1" min="0" value={settings.max_hallucination_retries} onChange={(e) => upd("max_hallucination_retries")(parseInt(e.target.value))} />
              </SettingRow>
            </CardContent>
          </AccordionContent>
        </AccordionItem>

        {/* 8. Debug */}
        <AccordionItem value="debug" className="border rounded-lg">
          <AccordionTrigger className="px-6 py-4 hover:no-underline">
            <CardTitle className="flex items-center gap-2 text-base"><Bug className="size-4" />Debug</CardTitle>
          </AccordionTrigger>
          <AccordionContent>
            <CardContent className="pt-0 space-y-1 divide-y divide-border">
              <SettingRow label="Log Level" description="Server-side log verbosity">
                <Select value={settings.log_level} onValueChange={upd("log_level") as (v: string) => void}>
                  <SelectTrigger><SelectValue /></SelectTrigger>
                  <SelectContent>
                    {["DEBUG", "INFO", "WARNING", "ERROR"].map((l) => (
                      <SelectItem key={l} value={l}>{l}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </SettingRow>
              <div className="py-2">
                <FlagRow id="f-debug-trace" label="Debug Trace" description="Emit per-step LangGraph trace logs" checked={settings.enable_debug_trace} onCheckedChange={upd("enable_debug_trace")} />
              </div>
            </CardContent>
          </AccordionContent>
        </AccordionItem>

        {/* 9. Appearance */}
        <AccordionItem value="appearance" className="border rounded-lg">
          <AccordionTrigger className="px-6 py-4 hover:no-underline">
            <CardTitle className="flex items-center gap-2 text-base"><Moon className="size-4" />Appearance</CardTitle>
          </AccordionTrigger>
          <AccordionContent>
            <CardContent className="pt-0">
              <div className="flex items-center gap-3">
                <Switch checked={true} disabled />
                <div>
                  <Label>Dark Mode</Label>
                  <p className="text-xs text-muted-foreground">Dark theme is the default and only supported mode.</p>
                </div>
              </div>
            </CardContent>
          </AccordionContent>
        </AccordionItem>

      </Accordion>

      <div className="flex gap-3 pb-8">
        <Button onClick={handleApplyToServer} disabled={applying}>
          {applying ? <Loader2 className="mr-2 size-4 animate-spin" /> : <Server className="mr-2 size-4" />}
          Apply to Server
        </Button>
        <Button variant="outline" onClick={handleReset}>
          <RotateCcw className="mr-2 size-4" />
          Reset to Defaults
        </Button>
      </div>
    </div>
  );
}
