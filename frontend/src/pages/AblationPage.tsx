import { useState } from "react";
import {
  FlaskConical,
  Play,
  Loader2,
  CheckCircle2,
  XCircle,
  Copy,
  ChevronRight,
  TableProperties,
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
import { Badge } from "@/components/ui/badge";
import { Switch } from "@/components/ui/switch";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from "@/components/ui/tabs";
import { Textarea } from "@/components/ui/textarea";
import { Separator } from "@/components/ui/separator";
import { Skeleton } from "@/components/ui/skeleton";
import {
  useAblationMatrix,
  useAblationDatasets,
  useAblationJobs,
  useAblationStatus,
  useRunPresetAblation,
  useRunCustomAblation,
  useAIJudgePayload,
} from "@/hooks/useAblation";
import { toast } from "sonner";
import type { AblationMatrixEntry, AblationJobResponse } from "@/types/api";

function StatusBadge({ status }: { status: string }) {
  const variantMap: Record<string, "default" | "secondary" | "destructive" | "outline"> = {
    done: "default",
    running: "secondary",
    failed: "destructive",
    queued: "outline",
  };
  const iconMap: Record<string, typeof CheckCircle2> = {
    done: CheckCircle2,
    running: Loader2,
    failed: XCircle,
    queued: Loader2,
  };
  const Icon = iconMap[status] ?? Loader2;
  return (
    <Badge variant={variantMap[status] ?? "outline"} className="gap-1">
      <Icon className={`size-3 ${status === "running" ? "animate-spin" : ""}`} />
      {status}
    </Badge>
  );
}

function MatrixBrowserTab() {
  const { data: matrix, isLoading } = useAblationMatrix();
  const runPreset = useRunPresetAblation();
  const [selectedStudy, setSelectedStudy] = useState<string | null>(null);

  if (isLoading) {
    return (
      <div className="space-y-3 p-4">
        {Array.from({ length: 5 }).map((_, i) => (
          <Skeleton key={i} className="h-12 w-full" />
        ))}
      </div>
    );
  }

  const handleRunPreset = (studyId: string) => {
    runPreset.mutate(
      { study_id: studyId },
      {
        onSuccess: () => {
          toast.success(`Study ${studyId} queued`);
          setSelectedStudy(null);
        },
      },
    );
  };

  return (
    <div className="space-y-4">
      <div className="rounded-md border border-border">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead className="w-24">Study ID</TableHead>
              <TableHead>Description</TableHead>
              <TableHead className="w-32">Env Overrides</TableHead>
              <TableHead className="w-20">RAGAS</TableHead>
              <TableHead className="w-24">Action</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {matrix?.map((entry: AblationMatrixEntry) => (
              <TableRow key={entry.study_id}>
                <TableCell className="font-mono font-medium text-xs">
                  {entry.study_id}
                </TableCell>
                <TableCell className="text-sm">{entry.description}</TableCell>
                <TableCell>
                  <div className="flex flex-wrap gap-1">
                    {Object.entries(entry.env_overrides)
                      .slice(0, 3)
                      .map(([k, v]) => (
                        <Badge key={k} variant="outline" className="text-[10px]">
                          {k.replace(/^(ENABLE_|RETRIEVAL_)/, "")}={v}
                        </Badge>
                      ))}
                    {Object.keys(entry.env_overrides).length > 3 && (
                      <Badge variant="outline" className="text-[10px]">
                        +{Object.keys(entry.env_overrides).length - 3} more
                      </Badge>
                    )}
                  </div>
                </TableCell>
                <TableCell>
                  {entry.run_ragas ? (
                    <Badge variant="default" className="text-[10px]">Yes</Badge>
                  ) : (
                    <Badge variant="outline" className="text-[10px]">No</Badge>
                  )}
                </TableCell>
                <TableCell>
                  <Button
                    size="xs"
                    onClick={() => handleRunPreset(entry.study_id)}
                    disabled={runPreset.isPending}
                  >
                    <Play className="mr-1 size-3" /> Run
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}

function RunExperimentTab() {
  const runPreset = useRunPresetAblation();
  const runCustom = useRunCustomAblation();
  const { data: datasets } = useAblationDatasets();

  const [presetStudyId, setPresetStudyId] = useState("");
  const [presetDataset, setPresetDataset] = useState(
    "tests/fixtures/01_basics_ecommerce/gold_standard.json",
  );

  const [customStudyId, setCustomStudyId] = useState("custom-run");
  const [customDataset, setCustomDataset] = useState(
    "tests/fixtures/01_basics_ecommerce/gold_standard.json",
  );
  const [customRetrievalMode, setCustomRetrievalMode] = useState<string>("");
  const [customEnableReranker, setCustomEnableReranker] = useState<boolean | null>(null);
  const [customEnableHallucinationGrader, setCustomEnableHallucinationGrader] = useState<boolean | null>(null);
  const [customEnableCypherHealing, setCustomEnableCypherHealing] = useState<boolean | null>(null);
  const [customEnableCriticValidation, setCustomEnableCriticValidation] = useState<boolean | null>(null);
  const [customChunkSize, setCustomChunkSize] = useState("");
  const [customErThreshold, setCustomErThreshold] = useState("");
  const [customSkipBuilder, setCustomSkipBuilder] = useState(false);
  const [customRunRagas, setCustomRunRagas] = useState(false);

  const handlePresetRun = () => {
    if (!presetStudyId) {
      toast.error("Please select a study ID");
      return;
    }
    runPreset.mutate(
      {
        study_id: presetStudyId,
        dataset: presetDataset,
      },
      {
        onSuccess: () => toast.success(`Preset ${presetStudyId} queued`),
      },
    );
  };

  const handleCustomRun = () => {
    runCustom.mutate(
      {
        study_id: customStudyId,
        dataset: customDataset,
        retrieval_mode: customRetrievalMode ? (customRetrievalMode as "hybrid" | "vector" | "bm25") : undefined,
        enable_reranker: customEnableReranker,
        enable_hallucination_grader: customEnableHallucinationGrader,
        enable_cypher_healing: customEnableCypherHealing,
        enable_critic_validation: customEnableCriticValidation,
        chunk_size: customChunkSize ? parseInt(customChunkSize) : undefined,
        er_similarity_threshold: customErThreshold ? parseFloat(customErThreshold) : undefined,
        skip_builder: customSkipBuilder,
        run_ragas: customRunRagas,
      },
      {
        onSuccess: () => toast.success(`Custom study ${customStudyId} queued`),
      },
    );
  };

  return (
    <div className="grid grid-cols-2 gap-6">
      {/* Preset Run */}
      <Card>
        <CardHeader>
          <CardTitle className="text-base">Preset Study</CardTitle>
          <CardDescription>Run a predefined AB-XX ablation.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Label>Study ID</Label>
            <Input
              placeholder="AB-00"
              value={presetStudyId}
              onChange={(e) => setPresetStudyId(e.target.value)}
            />
          </div>
          <div className="space-y-2">
            <Label>Dataset</Label>
            <Select value={presetDataset} onValueChange={setPresetDataset}>
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {datasets?.map((ds) => (
                  <SelectItem key={ds} value={ds}>
                    {ds.split("/").pop()?.replace("gold_standard.json", "") || ds}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
          <Button
            onClick={handlePresetRun}
            disabled={runPreset.isPending || !presetStudyId}
            className="w-full"
          >
            {runPreset.isPending ? (
              <Loader2 className="mr-2 size-4 animate-spin" />
            ) : (
              <Play className="mr-2 size-4" />
            )}
            Run Preset Study
          </Button>
        </CardContent>
      </Card>

      {/* Custom Run */}
      <Card>
        <CardHeader>
          <CardTitle className="text-base">Custom Study</CardTitle>
          <CardDescription>Configure your own ablation experiment.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-2 gap-3">
            <div className="space-y-2">
              <Label>Study ID</Label>
              <Input
                value={customStudyId}
                onChange={(e) => setCustomStudyId(e.target.value)}
              />
            </div>
            <div className="space-y-2">
              <Label>Dataset</Label>
              <Select value={customDataset} onValueChange={setCustomDataset}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {datasets?.map((ds) => (
                    <SelectItem key={ds} value={ds}>
                      {ds.split("/").pop()?.replace("gold_standard.json", "") || ds}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div className="space-y-2">
              <Label>Retrieval Mode</Label>
              <Select value={customRetrievalMode} onValueChange={setCustomRetrievalMode}>
                <SelectTrigger>
                  <SelectValue placeholder="Default" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="hybrid">Hybrid</SelectItem>
                  <SelectItem value="vector">Vector</SelectItem>
                  <SelectItem value="bm25">BM25</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-2">
              <Label>Chunk Size</Label>
              <Input
                type="number"
                value={customChunkSize}
                onChange={(e) => setCustomChunkSize(e.target.value)}
                placeholder="256"
              />
            </div>
          </div>

          <div className="space-y-2">
            <Label>ER Threshold</Label>
            <Input
              type="number"
              step="0.05"
              value={customErThreshold}
              onChange={(e) => setCustomErThreshold(e.target.value)}
              placeholder="0.75"
            />
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div className="flex items-center gap-2">
              <Switch
                checked={customEnableReranker ?? true}
                onCheckedChange={(v) => setCustomEnableReranker(v)}
              />
              <Label className="text-xs">Reranker</Label>
            </div>
            <div className="flex items-center gap-2">
              <Switch
                checked={customEnableHallucinationGrader ?? true}
                onCheckedChange={(v) => setCustomEnableHallucinationGrader(v)}
              />
              <Label className="text-xs">Hallucination Grader</Label>
            </div>
            <div className="flex items-center gap-2">
              <Switch
                checked={customEnableCypherHealing ?? true}
                onCheckedChange={(v) => setCustomEnableCypherHealing(v)}
              />
              <Label className="text-xs">Cypher Healing</Label>
            </div>
            <div className="flex items-center gap-2">
              <Switch
                checked={customEnableCriticValidation ?? true}
                onCheckedChange={(v) => setCustomEnableCriticValidation(v)}
              />
              <Label className="text-xs">Critic Validation</Label>
            </div>
            <div className="flex items-center gap-2">
              <Switch
                checked={customSkipBuilder}
                onCheckedChange={setCustomSkipBuilder}
              />
              <Label className="text-xs">Skip Builder</Label>
            </div>
            <div className="flex items-center gap-2">
              <Switch
                checked={customRunRagas}
                onCheckedChange={setCustomRunRagas}
              />
              <Label className="text-xs">Run RAGAS</Label>
            </div>
          </div>

          <Button
            onClick={handleCustomRun}
            disabled={runCustom.isPending}
            className="w-full"
          >
            {runCustom.isPending ? (
              <Loader2 className="mr-2 size-4 animate-spin" />
            ) : (
              <Play className="mr-2 size-4" />
            )}
            Run Custom Study
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}

function ResultsTab() {
  const { data: jobs, isLoading } = useAblationJobs();
  const [selectedJobId, setSelectedJobId] = useState<string | null>(null);
  const { data: result } = useAblationStatus(selectedJobId);

  if (isLoading) {
    return (
      <div className="space-y-3 p-4">
        {Array.from({ length: 4 }).map((_, i) => (
          <Skeleton key={i} className="h-10 w-full" />
        ))}
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="rounded-md border border-border">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Job ID</TableHead>
              <TableHead>Study ID</TableHead>
              <TableHead>Status</TableHead>
              <TableHead>Dataset</TableHead>
              <TableHead>Action</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {jobs && jobs.length > 0 ? (
              jobs.map((job: AblationJobResponse) => (
                <TableRow key={job.job_id}>
                  <TableCell className="font-mono text-xs">
                    {job.job_id.slice(0, 8)}...
                  </TableCell>
                  <TableCell className="text-sm font-medium">
                    {job.study_id}
                  </TableCell>
                  <TableCell>
                    <StatusBadge status={job.status} />
                  </TableCell>
                  <TableCell className="text-xs text-muted-foreground">
                    {job.dataset.split("/").pop() || job.dataset}
                  </TableCell>
                  <TableCell>
                    <Button
                      size="xs"
                      variant="outline"
                      onClick={() => setSelectedJobId(job.job_id)}
                    >
                      <ChevronRight className="mr-1 size-3" /> Details
                    </Button>
                  </TableCell>
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell
                  colSpan={5}
                  className="text-center text-sm text-muted-foreground py-8"
                >
                  No ablation jobs yet. Run an experiment to see results here.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>

      {result && selectedJobId && (
        <Card>
          <CardHeader>
            <CardTitle className="text-base">
              Result: {result.study_id}
            </CardTitle>
            <CardDescription>Job {selectedJobId.slice(0, 12)}...</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {result.error && (
              <div className="rounded-md bg-destructive/10 p-3 text-sm text-destructive">
                {result.error}
              </div>
            )}

            {result.summary && (
              <div>
                <h4 className="mb-2 text-sm font-medium">Summary</h4>
                <div className="grid grid-cols-4 gap-3">
                  {Object.entries(result.summary).map(([key, value]) => (
                    <div key={key} className="rounded border border-border p-2">
                      <p className="text-[10px] text-muted-foreground">
                        {key.replace(/_/g, " ")}
                      </p>
                      <p className="text-sm font-semibold">
                        {typeof value === "number"
                          ? value % 1 !== 0
                            ? value.toFixed(3)
                            : value.toLocaleString()
                          : String(value ?? "-")}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {result.ragas && (
              <div>
                <h4 className="mb-2 text-sm font-medium">RAGAS Metrics</h4>
                <div className="grid grid-cols-4 gap-3">
                  {Object.entries(result.ragas).map(([key, value]) => (
                    <div key={key} className="rounded border border-border p-2">
                      <p className="text-[10px] text-muted-foreground">
                        {key.replace(/_/g, " ")}
                      </p>
                      <p className="text-sm font-semibold">
                        {(value as number).toFixed(4)}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {result.bundle_path && (
              <div className="rounded border border-border bg-muted/30 p-3">
                <p className="text-xs text-muted-foreground">Bundle Path</p>
                <p className="font-mono text-xs">{result.bundle_path}</p>
              </div>
            )}
          </CardContent>
        </Card>
      )}
    </div>
  );
}

function AIJudgeTab() {
  const [studyId, setStudyId] = useState("");
  const [datasetId, setDatasetId] = useState("");
  const [fetchTriggered, setFetchTriggered] = useState(false);

  const { data, isLoading } = useAIJudgePayload(
    fetchTriggered ? studyId : null,
    fetchTriggered ? datasetId : null,
  );

  const handleFetch = () => {
    if (!studyId || !datasetId) {
      toast.error("Please enter both Study ID and Dataset ID");
      return;
    }
    setFetchTriggered(true);
  };

  const handleCopy = async (text: string) => {
    try {
      await navigator.clipboard.writeText(text);
      toast.success("Copied to clipboard");
    } catch {
      toast.error("Failed to copy");
    }
  };

  return (
    <div className="space-y-4">
      <Card>
        <CardHeader>
          <CardTitle className="text-base">AI-as-Judge Evaluation</CardTitle>
          <CardDescription>
            Generate the AI Judge payload from an evaluation bundle.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label>Study ID</Label>
              <Input
                placeholder="AB-00"
                value={studyId}
                onChange={(e) => setStudyId(e.target.value)}
              />
            </div>
            <div className="space-y-2">
              <Label>Dataset ID</Label>
              <Input
                placeholder="01_basics_ecommerce"
                value={datasetId}
                onChange={(e) => setDatasetId(e.target.value)}
              />
            </div>
          </div>
          <Button onClick={handleFetch} disabled={isLoading}>
            {isLoading ? (
              <Loader2 className="mr-2 size-4 animate-spin" />
            ) : (
              <TableProperties className="mr-2 size-4" />
            )}
            Fetch Judge Payload
          </Button>
        </CardContent>
      </Card>

      {data && (
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle className="text-base">Judge Payload</CardTitle>
              <Button
                variant="outline"
                size="sm"
                onClick={() => handleCopy(JSON.stringify(data, null, 2))}
              >
                <Copy className="mr-1 size-3" /> Copy All
              </Button>
            </div>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <div className="flex items-center justify-between mb-2">
                <Label className="text-xs font-medium">Instructions</Label>
                <Button
                  variant="ghost"
                  size="xs"
                  onClick={() => handleCopy(data.instructions)}
                >
                  <Copy className="size-3" />
                </Button>
              </div>
              <p className="rounded border border-border bg-muted/30 p-3 text-xs text-muted-foreground">
                {data.instructions}
              </p>
            </div>

            <Separator />

            <div>
              <div className="flex items-center justify-between mb-2">
                <Label className="text-xs font-medium">System Prompt</Label>
                <Button
                  variant="ghost"
                  size="xs"
                  onClick={() => handleCopy(data.system_prompt)}
                >
                  <Copy className="size-3" />
                </Button>
              </div>
              <Textarea
                readOnly
                value={data.system_prompt.slice(0, 2000) + (data.system_prompt.length > 2000 ? "\n..." : "")}
                className="h-48 font-mono text-xs"
              />
            </div>

            <Separator />

            <div>
              <div className="flex items-center justify-between mb-2">
                <Label className="text-xs font-medium">Evaluation Bundle</Label>
                <Button
                  variant="ghost"
                  size="xs"
                  onClick={() =>
                    handleCopy(JSON.stringify(data.evaluation_bundle, null, 2))
                  }
                >
                  <Copy className="size-3" />
                </Button>
              </div>
              <Textarea
                readOnly
                value={JSON.stringify(data.evaluation_bundle, null, 2).slice(0, 3000) + "..."}
                className="h-64 font-mono text-xs"
              />
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}

export function AblationPage() {
  return (
    <div className="p-6 space-y-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight">Ablation Studies</h1>
        <p className="text-sm text-muted-foreground">
          Run and analyze ablation experiments on the GraphRAG pipeline.
        </p>
      </div>

      <Tabs defaultValue="matrix" className="space-y-4">
        <TabsList>
          <TabsTrigger value="matrix">
            <TableProperties className="mr-1 size-3.5" />
            Matrix Browser
          </TabsTrigger>
          <TabsTrigger value="run">
            <Play className="mr-1 size-3.5" />
            Run Experiment
          </TabsTrigger>
          <TabsTrigger value="results">
            <FlaskConical className="mr-1 size-3.5" />
            Results
          </TabsTrigger>
          <TabsTrigger value="judge">
            <Copy className="mr-1 size-3.5" />
            AI Judge
          </TabsTrigger>
        </TabsList>

        <TabsContent value="matrix">
          <MatrixBrowserTab />
        </TabsContent>

        <TabsContent value="run">
          <RunExperimentTab />
        </TabsContent>

        <TabsContent value="results">
          <ResultsTab />
        </TabsContent>

        <TabsContent value="judge">
          <AIJudgeTab />
        </TabsContent>
      </Tabs>
    </div>
  );
}
