import { useState, useCallback, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { useAppState } from "@/contexts/AppStateContext";
import {
  Upload,
  FileText,
  Database,
  Loader2,
  CheckCircle2,
  XCircle,
  ChevronDown,
  Play,
  Trash2,
  Network,
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
import { Badge } from "@/components/ui/badge";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Separator } from "@/components/ui/separator";
import { useStartBuildUpload, useBuildStatus } from "@/hooks/useJobs";

function FileUploadZone({
  label,
  accept,
  files,
  onFilesChange,
  icon: Icon,
}: {
  label: string;
  accept: string;
  files: File[];
  onFilesChange: (files: File[]) => void;
  icon: React.ElementType;
}) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [dragOver, setDragOver] = useState(false);

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      setDragOver(false);
      const dropped = Array.from(e.dataTransfer.files);
      onFilesChange([...files, ...dropped]);
    },
    [files, onFilesChange],
  );

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(true);
  }, []);

  const handleDragLeave = useCallback(() => {
    setDragOver(false);
  }, []);

  const handleInputChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      if (e.target.files) {
        onFilesChange([...files, ...Array.from(e.target.files)]);
      }
    },
    [files, onFilesChange],
  );

  const removeFile = useCallback(
    (index: number) => {
      onFilesChange(files.filter((_, i) => i !== index));
    },
    [files, onFilesChange],
  );

  return (
    <div className="space-y-3">
      <Label className="flex items-center gap-2 text-sm font-medium">
        <Icon className="size-4" />
        {label}
      </Label>
      <div
        className={`flex min-h-[140px] cursor-pointer flex-col items-center justify-center rounded-lg border-2 border-dashed p-4 transition-colors ${
          dragOver
            ? "border-primary bg-primary/10"
            : "border-border hover:border-muted-foreground"
        }`}
        onClick={() => inputRef.current?.click()}
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
      >
        <Upload className="mb-2 size-8 text-muted-foreground" />
        <p className="text-sm text-muted-foreground">
          Drag & drop or click to upload
        </p>
        <p className="text-xs text-muted-foreground">Accepts: {accept}</p>
        <input
          ref={inputRef}
          type="file"
          accept={accept}
          multiple
          className="hidden"
          onChange={handleInputChange}
        />
      </div>
      {files.length > 0 && (
        <div className="space-y-1.5">
          {files.map((file, i) => (
            <div
              key={`${file.name}-${i}`}
              className="flex items-center justify-between rounded-md border border-border bg-muted/50 px-3 py-1.5"
            >
              <span className="max-w-[200px] truncate text-xs font-mono">
                {file.name}
              </span>
              <div className="flex items-center gap-2">
                <span className="text-xs text-muted-foreground">
                  {(file.size / 1024).toFixed(1)} KB
                </span>
                <Button
                  variant="ghost"
                  size="icon-xs"
                  onClick={(e) => {
                    e.stopPropagation();
                    removeFile(i);
                  }}
                >
                  <Trash2 className="size-3 text-destructive" />
                </Button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

function BuildSteps({ data }: { data: { status: string; triplets_extracted?: number | null; entities_resolved?: number | null; tables_parsed?: number | null; tables_completed?: number | null; current_step?: string | null } }) {
  const steps = [
    { label: "Queued", done: true },
    { label: "Parse & Extract", done: (data.triplets_extracted ?? 0) > 0 },
    { label: "Entity Resolution", done: (data.entities_resolved ?? 0) > 0 },
    { label: "Schema Mapping", done: (data.tables_completed ?? 0) > 0 },
    { label: "Graph Build", done: data.status === "done" },
  ];

  const currentStep = [...steps].reverse().findIndex((s) => s.done);
  const activeIdx = currentStep === -1 ? 0 : steps.length - 1 - currentStep + 1;

  return (
    <div className="space-y-2">
      {data.current_step && data.status === "running" && (
        <p className="text-xs text-muted-foreground">
          Current node: <span className="text-primary font-mono">{data.current_step}</span>
        </p>
      )}
    <ol className="flex items-center gap-0">
      {steps.map((step, i) => {
        const isActive = i === activeIdx && data.status !== "done";
        const isDone = step.done;
        return (
          <li key={step.label} className="flex flex-1 items-center">
            <div className="flex flex-col items-center gap-1 min-w-0">
              <div
                className={`flex size-6 items-center justify-center rounded-full border text-[10px] font-semibold shrink-0 ${
                  isDone
                    ? "border-emerald-500 bg-emerald-500/15 text-emerald-400"
                    : isActive
                      ? "border-primary bg-primary/15 text-primary"
                      : "border-border text-muted-foreground"
                }`}
              >
                {isDone ? "✓" : i + 1}
              </div>
              <span className={`text-[10px] text-center truncate px-0.5 ${isDone ? "text-emerald-400" : isActive ? "text-primary" : "text-muted-foreground"}`}>
                {step.label}
              </span>
            </div>
            {i < steps.length - 1 && (
              <div className={`h-px flex-1 mx-1 mb-3 ${isDone ? "bg-emerald-500/50" : "bg-border"}`} />
            )}
          </li>
        );
      })}
    </ol>
    </div>
  );
}

function BuildMetricsCard({ jobId }: { jobId: string }) {
  const { data, isLoading } = useBuildStatus(jobId);

  if (isLoading && !data) {
    return (
      <Card>
        <CardContent className="flex items-center justify-center py-8">
          <Loader2 className="size-6 animate-spin text-muted-foreground" />
        </CardContent>
      </Card>
    );
  }

  if (!data) return null;

  const statusIcon =
    data.status === "done" ? (
      <CheckCircle2 className="size-5 text-emerald-400" />
    ) : data.status === "failed" ? (
      <XCircle className="size-5 text-red-400" />
    ) : (
      <Loader2 className="size-5 animate-spin text-blue-400" />
    );

  const statusColor =
    data.status === "done"
      ? "text-emerald-400"
      : data.status === "failed"
        ? "text-red-400"
        : "text-blue-400";

  const metrics = [
    { label: "Triplets Extracted", value: data.triplets_extracted },
    { label: "Entities Resolved", value: data.entities_resolved },
    { label: "Tables Parsed", value: data.tables_parsed },
    { label: "Tables Completed", value: data.tables_completed },
    { label: "Parent Chunks", value: data.parent_chunks },
    { label: "Child Chunks", value: data.child_chunks },
  ];

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="text-base">Build Status</CardTitle>
          <div className="flex items-center gap-2">
            {statusIcon}
            <span className={`text-sm font-medium capitalize ${statusColor}`}>
              {data.status}
            </span>
          </div>
        </div>
        <CardDescription>Job ID: {data.job_id?.slice(0, 12) ?? "—"}...</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        {data.error && (
          <div className="rounded-md bg-destructive/10 p-3 text-sm text-destructive">
            {data.error}
          </div>
        )}

        {data.status === "done" && (
          <div className="grid grid-cols-3 gap-3">
            {metrics.map((m) => (
              <div
                key={m.label}
                className="rounded-md border border-border p-3"
              >
                <p className="text-xs text-muted-foreground">{m.label}</p>
                <p className="text-lg font-semibold">
                  {m.value?.toLocaleString() ?? "-"}
                </p>
              </div>
            ))}
          </div>
        )}

        {(data.status === "running" || data.status === "queued") && (
          <div className="space-y-3">
            <BuildSteps data={data} />
          </div>
        )}
      </CardContent>
    </Card>
  );
}

export function KGBuilderPage() {
  const navigate = useNavigate();
  const startBuild = useStartBuildUpload();

  const [docFiles, setDocFiles] = useState<File[]>([]);
  const [ddlFiles, setDdlFiles] = useState<File[]>([]);
  const [studyId, setStudyId] = useState("demo");
  const [clearGraph, setClearGraph] = useState(true);
  const [lazyExtraction, setLazyExtraction] = useState(false);
  const { activeBuildJobId: activeJobId, setActiveBuildJobId: setActiveJobId } = useAppState();

  // Advanced config
  const [retrievalMode, setRetrievalMode] = useState<string>("hybrid");
  const [enableReranker, setEnableReranker] = useState(true);
  const [enableSchemaEnrichment, setEnableSchemaEnrichment] = useState(true);
  const [enableCriticValidation, setEnableCriticValidation] = useState(true);
  const [enableCypherHealing, setEnableCypherHealing] = useState(true);
  const [enableHallucinationGrader, setEnableHallucinationGrader] = useState(true);
  const [chunkSize, setChunkSize] = useState("256");
  const [chunkOverlap, setChunkOverlap] = useState("32");
  const [erThreshold, setErThreshold] = useState("0.75");

  const handleStartBuild = async () => {
    if (docFiles.length === 0 && ddlFiles.length === 0) {
      return;
    }

    try {
      const result = await startBuild.mutateAsync({
        docFiles: docFiles,
        ddlFiles: ddlFiles,
        options: {
          clear_graph: clearGraph,
          study_id: studyId,
          lazy_extraction: lazyExtraction,
        },
      });
      setActiveJobId(result.job_id);
    } catch {
      // Error is handled by the mutation's onError
    }
  };

  return (
    <div className="p-6 space-y-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight">KG Builder</h1>
        <p className="text-sm text-muted-foreground">
          Upload documentation and DDL files to build the Knowledge Graph.
        </p>
      </div>

      {/* File upload zones */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <Card>
          <CardContent className="pt-6">
            <FileUploadZone
              label="Business Documentation"
              accept=".pdf,.md,.txt"
              files={docFiles}
              onFilesChange={setDocFiles}
              icon={FileText}
            />
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <FileUploadZone
              label="DDL SQL Files"
              accept=".sql"
              files={ddlFiles}
              onFilesChange={setDdlFiles}
              icon={Database}
            />
          </CardContent>
        </Card>
      </div>

      {/* Build config */}
      <Card>
        <CardHeader>
          <CardTitle className="text-base">Build Configuration</CardTitle>
          <CardDescription>Basic settings for the build run.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-3 gap-4">
            <div className="space-y-2">
              <Label htmlFor="study-id">Study ID</Label>
              <Input
                id="study-id"
                value={studyId}
                onChange={(e) => setStudyId(e.target.value)}
                placeholder="demo"
              />
            </div>

            <div className="flex items-center gap-3 pt-6">
              <Switch
                id="clear-graph"
                checked={clearGraph}
                onCheckedChange={setClearGraph}
              />
              <Label htmlFor="clear-graph">Clear Graph</Label>
              <Badge variant="outline" className="text-xs">
                Recommended
              </Badge>
            </div>

            <div className="flex items-center gap-3 pt-6">
              <Switch
                id="lazy-extraction"
                checked={lazyExtraction}
                onCheckedChange={setLazyExtraction}
              />
              <Label htmlFor="lazy-extraction">Lazy Extraction</Label>
            </div>
          </div>

          <Separator />

          {/* Advanced config */}
          <Accordion openMultiple={false}>
            <AccordionItem value="advanced" className="border-none">
              <AccordionTrigger className="py-2 text-sm text-muted-foreground hover:no-underline">
                <span className="flex items-center gap-2">
                  <ChevronDown className="size-4" />
                  Advanced Configuration
                </span>
              </AccordionTrigger>
              <AccordionContent className="space-y-4 pt-2">
                <div className="grid grid-cols-3 gap-4">
                  <div className="space-y-2">
                    <Label>Retrieval Mode</Label>
                    <Select value={retrievalMode} onValueChange={setRetrievalMode}>
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="hybrid">Hybrid</SelectItem>
                        <SelectItem value="vector">Vector Only</SelectItem>
                        <SelectItem value="bm25">BM25 Only</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="chunk-size">Chunk Size</Label>
                    <Input
                      id="chunk-size"
                      type="number"
                      value={chunkSize}
                      onChange={(e) => setChunkSize(e.target.value)}
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="chunk-overlap">Chunk Overlap</Label>
                    <Input
                      id="chunk-overlap"
                      type="number"
                      value={chunkOverlap}
                      onChange={(e) => setChunkOverlap(e.target.value)}
                    />
                  </div>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="er-threshold">ER Similarity Threshold</Label>
                  <Input
                    id="er-threshold"
                    type="number"
                    step="0.05"
                    value={erThreshold}
                    onChange={(e) => setErThreshold(e.target.value)}
                  />
                </div>

                <div className="grid grid-cols-3 gap-4">
                  <div className="flex items-center gap-2">
                    <Switch
                      id="enable-reranker"
                      checked={enableReranker}
                      onCheckedChange={setEnableReranker}
                    />
                    <Label htmlFor="enable-reranker">Reranker</Label>
                  </div>
                  <div className="flex items-center gap-2">
                    <Switch
                      id="enable-schema-enrich"
                      checked={enableSchemaEnrichment}
                      onCheckedChange={setEnableSchemaEnrichment}
                    />
                    <Label htmlFor="enable-schema-enrich">Schema Enrichment</Label>
                  </div>
                  <div className="flex items-center gap-2">
                    <Switch
                      id="enable-critic"
                      checked={enableCriticValidation}
                      onCheckedChange={setEnableCriticValidation}
                    />
                    <Label htmlFor="enable-critic">Critic Validation</Label>
                  </div>
                  <div className="flex items-center gap-2">
                    <Switch
                      id="enable-cypher-healing"
                      checked={enableCypherHealing}
                      onCheckedChange={setEnableCypherHealing}
                    />
                    <Label htmlFor="enable-cypher-healing">Cypher Healing</Label>
                  </div>
                  <div className="flex items-center gap-2">
                    <Switch
                      id="enable-hallucination"
                      checked={enableHallucinationGrader}
                      onCheckedChange={setEnableHallucinationGrader}
                    />
                    <Label htmlFor="enable-hallucination">Hallucination Grader</Label>
                  </div>
                </div>
              </AccordionContent>
            </AccordionItem>
          </Accordion>
        </CardContent>
      </Card>

      {/* Build status + Start button */}
      <div className="flex items-start gap-4">
        <Button
          size="lg"
          onClick={handleStartBuild}
          disabled={
            startBuild.isPending ||
            (docFiles.length === 0 && ddlFiles.length === 0)
          }
        >
          {startBuild.isPending ? (
            <Loader2 className="mr-2 size-4 animate-spin" />
          ) : (
            <Play className="mr-2 size-4" />
          )}
          Start Build
        </Button>

        <Button
          variant="outline"
          size="lg"
          onClick={() => navigate("/graph")}
          disabled={!activeJobId}
        >
          <Network className="mr-2 size-4" />
          View Graph
        </Button>
      </div>

      {activeJobId && <BuildMetricsCard jobId={activeJobId} />}
    </div>
  );
}
