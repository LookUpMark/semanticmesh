import { useState } from "react";
import {
  Save,
  RotateCcw,
  Wifi,
  WifiOff,
  Cpu,
  Sliders,
  ToggleLeft,
  Moon,
  CheckCircle2,
  Loader2,
} from "lucide-react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Separator } from "@/components/ui/separator";
import { useSettings } from "@/contexts/SettingsContext";
import { useHealth } from "@/hooks/useJobs";
import { toast } from "sonner";

interface FeatureFlag {
  key: string;
  label: string;
  description: string;
  defaultValue: boolean;
}

const FEATURE_FLAGS: FeatureFlag[] = [
  {
    key: "enable_schema_enrichment",
    label: "Schema Enrichment",
    description: "LLM acronym expansion during schema enrichment",
    defaultValue: true,
  },
  {
    key: "enable_cypher_healing",
    label: "Cypher Healing",
    description: "Auto-fix Cypher syntax errors via LLM reflection",
    defaultValue: true,
  },
  {
    key: "enable_critic_validation",
    label: "Critic Validation",
    description: "Actor-Critic mapping validation loop",
    defaultValue: true,
  },
  {
    key: "enable_hallucination_grader",
    label: "Hallucination Grader",
    description: "Self-RAG hallucination grading",
    defaultValue: true,
  },
  {
    key: "enable_reranker",
    label: "Reranker",
    description: "Cross-encoder reranking (bge-reranker-v2-m3)",
    defaultValue: true,
  },
  {
    key: "enable_retrieval_quality_gate",
    label: "Retrieval Quality Gate",
    description: "Retrieval quality gate before generation",
    defaultValue: true,
  },
  {
    key: "enable_grader_consistency_validator",
    label: "Grader Consistency",
    description: "Grader consistency check across iterations",
    defaultValue: true,
  },
  {
    key: "enable_spacy_heuristics",
    label: "spaCy Heuristics",
    description: "spaCy-based heuristic extraction as fallback",
    defaultValue: true,
  },
  {
    key: "enable_lazy_expansion",
    label: "Lazy Expansion",
    description: "Lazy context expansion strategy",
    defaultValue: true,
  },
  {
    key: "use_lazy_extraction",
    label: "Lazy Extraction",
    description: "Use rule-based extraction instead of LLM",
    defaultValue: false,
  },
];

interface PipelineSetting {
  key: string;
  label: string;
  type: "text" | "number" | "select";
  defaultValue: string;
  description: string;
  options?: string[];
  step?: string;
}

const PIPELINE_SETTINGS: PipelineSetting[] = [
  {
    key: "llm_model_reasoning",
    label: "Reasoning Model",
    type: "text",
    defaultValue: "openai/gpt-oss-120b",
    description: "Main reasoning/generation model",
  },
  {
    key: "llm_model_extraction",
    label: "Extraction Model",
    type: "text",
    defaultValue: "openai/gpt-4.1-nano",
    description: "JSON extraction model",
  },
  {
    key: "llm_model_midtier",
    label: "Midtier Model",
    type: "text",
    defaultValue: "openai/gpt-4.1-nano",
    description: "RAG mapping, Actor-Critic, hallucination grading",
  },
  {
    key: "temperature_extraction",
    label: "Extraction Temperature",
    type: "number",
    defaultValue: "0.0",
    description: "0.0 = deterministic JSON",
    step: "0.1",
  },
  {
    key: "temperature_reasoning",
    label: "Reasoning Temperature",
    type: "number",
    defaultValue: "0.0",
    description: "0.0 = deterministic",
    step: "0.1",
  },
  {
    key: "temperature_generation",
    label: "Generation Temperature",
    type: "number",
    defaultValue: "0.3",
    description: "0.3 for fluency",
    step: "0.1",
  },
  {
    key: "max_tokens_extraction",
    label: "Max Tokens Extraction",
    type: "number",
    defaultValue: "8192",
    description: "Max output tokens for extraction LLM",
  },
  {
    key: "max_tokens_reasoning",
    label: "Max Tokens Reasoning",
    type: "number",
    defaultValue: "4096",
    description: "Max output tokens for reasoning LLM",
  },
  {
    key: "chunk_size",
    label: "Chunk Size",
    type: "number",
    defaultValue: "256",
    description: "Child chunk token size",
  },
  {
    key: "chunk_overlap",
    label: "Chunk Overlap",
    type: "number",
    defaultValue: "32",
    description: "Child chunk overlap in tokens",
  },
  {
    key: "retrieval_mode",
    label: "Retrieval Mode",
    type: "select",
    defaultValue: "hybrid",
    description: "Retrieval channel combination",
    options: ["hybrid", "vector", "bm25"],
  },
  {
    key: "er_similarity_threshold",
    label: "ER Similarity Threshold",
    type: "number",
    defaultValue: "0.75",
    description: "Cosine similarity for entity blocking",
    step: "0.05",
  },
  {
    key: "confidence_threshold",
    label: "Confidence Threshold",
    type: "number",
    defaultValue: "0.90",
    description: "Mapping confidence for HITL interrupt",
    step: "0.05",
  },
  {
    key: "max_reflection_attempts",
    label: "Max Reflection Attempts",
    type: "number",
    defaultValue: "3",
    description: "Actor-Critic reflection retries",
  },
  {
    key: "max_cypher_healing_attempts",
    label: "Max Cypher Healing",
    type: "number",
    defaultValue: "3",
    description: "Cypher healing retries before fallback",
  },
];

export function SettingsPage() {
  const { apiKey, apiBaseUrl, setApiKey, setApiBaseUrl } = useSettings();
  const { data: health } = useHealth();
  const [connectionTesting, setConnectionTesting] = useState(false);

  const [localApiKey, setLocalApiKey] = useState(apiKey);
  const [localBaseUrl, setLocalBaseUrl] = useState(apiBaseUrl);

  const [pipelineValues, setPipelineValues] = useState<Record<string, string>>(
    () => {
      const initial: Record<string, string> = {};
      PIPELINE_SETTINGS.forEach((s) => {
        initial[s.key] = s.defaultValue;
      });
      return initial;
    },
  );

  const [featureFlags, setFeatureFlags] = useState<Record<string, boolean>>(
    () => {
      const initial: Record<string, boolean> = {};
      FEATURE_FLAGS.forEach((f) => {
        initial[f.key] = f.defaultValue;
      });
      return initial;
    },
  );

  const handleTestConnection = async () => {
    setConnectionTesting(true);
    try {
      const res = await fetch(
        localBaseUrl.replace(/\/api\/v1\/?$/, "") + "/health",
      );
      const data = await res.json();
      if (data.status === "ok" || data.status === "healthy") {
        toast.success("Connection successful", {
          description: "API is reachable and healthy.",
        });
      } else {
        toast.warning("Connection unstable", {
          description: `API returned status: ${data.status}`,
        });
      }
    } catch {
      toast.error("Connection failed", {
        description: "Could not reach the API server.",
      });
    } finally {
      setConnectionTesting(false);
    }
  };

  const handleSave = () => {
    setApiKey(localApiKey);
    setApiBaseUrl(localBaseUrl);
    toast.success("Settings saved", {
      description: "API configuration has been updated.",
    });
  };

  const handleReset = () => {
    const defaults: Record<string, string> = {};
    PIPELINE_SETTINGS.forEach((s) => {
      defaults[s.key] = s.defaultValue;
    });
    setPipelineValues(defaults);

    const flagDefaults: Record<string, boolean> = {};
    FEATURE_FLAGS.forEach((f) => {
      flagDefaults[f.key] = f.defaultValue;
    });
    setFeatureFlags(flagDefaults);

    setLocalApiKey("");
    setLocalBaseUrl("/api/v1");

    toast.info("Settings reset", {
      description: "All values have been restored to defaults.",
    });
  };

  const systemOk = health?.status === "ok" || health?.status === "healthy";

  return (
    <div className="p-6 space-y-6 max-w-4xl">
      <div>
        <h1 className="text-2xl font-bold tracking-tight">Settings</h1>
        <p className="text-sm text-muted-foreground">
          Configure the GraphRAG Studio API connection and pipeline parameters.
        </p>
      </div>

      {/* API Connection */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-base">
            {systemOk ? (
              <Wifi className="size-4 text-emerald-400" />
            ) : (
              <WifiOff className="size-4 text-red-400" />
            )}
            API Connection
          </CardTitle>
          <CardDescription>
            Configure the backend API endpoint and authentication.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="api-base-url">Base URL</Label>
              <Input
                id="api-base-url"
                value={localBaseUrl}
                onChange={(e) => setLocalBaseUrl(e.target.value)}
                placeholder="http://localhost:8000/api/v1"
              />
              <p className="text-xs text-muted-foreground">
                VITE_API_BASE_URL or proxy target
              </p>
            </div>
            <div className="space-y-2">
              <Label htmlFor="api-key">API Key</Label>
              <Input
                id="api-key"
                type="password"
                value={localApiKey}
                onChange={(e) => setLocalApiKey(e.target.value)}
                placeholder="Optional X-API-Key header"
              />
              <p className="text-xs text-muted-foreground">
                Leave empty if auth is disabled on the server.
              </p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <Button
              variant="outline"
              onClick={handleTestConnection}
              disabled={connectionTesting}
            >
              {connectionTesting ? (
                <Loader2 className="mr-2 size-4 animate-spin" />
              ) : systemOk ? (
                <CheckCircle2 className="mr-2 size-4 text-emerald-400" />
              ) : (
                <Wifi className="mr-2 size-4" />
              )}
              Test Connection
            </Button>
            {health && (
              <span
                className={`text-sm ${systemOk ? "text-emerald-400" : "text-red-400"}`}
              >
                {systemOk ? "Connected" : "Disconnected"}
              </span>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Pipeline Configuration */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-base">
            <Cpu className="size-4" />
            Pipeline Configuration
          </CardTitle>
          <CardDescription>
            LLM models, temperatures, chunking, retrieval, and validation parameters.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {PIPELINE_SETTINGS.map((setting, idx) => (
            <div key={setting.key}>
              {idx > 0 && idx % 4 === 0 && <Separator className="my-3" />}
              <div className="grid grid-cols-3 gap-4 items-center">
                <div>
                  <Label className="text-sm">{setting.label}</Label>
                  <p className="text-xs text-muted-foreground">
                    {setting.description}
                  </p>
                </div>
                <div className="col-span-2">
                  {setting.type === "select" && setting.options ? (
                    <Select
                      value={pipelineValues[setting.key]}
                      onValueChange={(v) =>
                        setPipelineValues((prev) => ({ ...prev, [setting.key]: v }))
                      }
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        {setting.options.map((opt) => (
                          <SelectItem key={opt} value={opt}>
                            {opt}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  ) : (
                    <Input
                      type={setting.type}
                      step={setting.step}
                      value={pipelineValues[setting.key]}
                      onChange={(e) =>
                        setPipelineValues((prev) => ({
                          ...prev,
                          [setting.key]: e.target.value,
                        }))
                      }
                    />
                  )}
                </div>
              </div>
            </div>
          ))}
        </CardContent>
      </Card>

      {/* Feature Flags */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-base">
            <ToggleLeft className="size-4" />
            Feature Flags
          </CardTitle>
          <CardDescription>
            Enable or disable pipeline components for ablation experiments.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 gap-x-8 gap-y-4">
            {FEATURE_FLAGS.map((flag) => (
              <div key={flag.key} className="flex items-start gap-3">
                <Switch
                  id={flag.key}
                  checked={featureFlags[flag.key]}
                  onCheckedChange={(checked) =>
                    setFeatureFlags((prev) => ({ ...prev, [flag.key]: checked }))
                  }
                  className="mt-0.5"
                />
                <div>
                  <Label htmlFor={flag.key} className="text-sm cursor-pointer">
                    {flag.label}
                  </Label>
                  <p className="text-xs text-muted-foreground">
                    {flag.description}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Appearance */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-base">
            <Moon className="size-4" />
            Appearance
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center gap-3">
            <Switch checked={true} disabled />
            <div>
              <Label>Dark Mode</Label>
              <p className="text-xs text-muted-foreground">
                Dark theme is the default and only supported mode.
              </p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Action Buttons */}
      <div className="flex gap-3">
        <Button onClick={handleSave}>
          <Save className="mr-2 size-4" />
          Save Settings
        </Button>
        <Button variant="outline" onClick={handleReset}>
          <RotateCcw className="mr-2 size-4" />
          Reset to Defaults
        </Button>
      </div>
    </div>
  );
}
