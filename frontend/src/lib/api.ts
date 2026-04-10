import axios from "axios";
import type {
  BuildRequest,
  BuildResultResponse,
  QueryRequest,
  QueryResponse,
  PipelineRequest,
  PipelineJobResponse,
  PipelineResultResponse,
  GraphStatsResponse,
  GraphDataResponse,
  DemoJob,
  CustomAblationRequest,
  PresetAblationRequest,
  AblationJobResponse,
  PresetAblationJobResponse,
  AblationResultResponse,
  AblationMatrixEntry,
  AIJudgePayload,
  KGSnapshotMeta,
  SaveSnapshotRequest,
} from "@/types/api";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "/api/v1",
  headers: {
    "Content-Type": "application/json",
  },
});

api.interceptors.request.use((config) => {
  const apiKey =
    import.meta.env.VITE_API_KEY || localStorage.getItem("thesis_api_key");
  if (apiKey) {
    config.headers["X-API-Key"] = apiKey;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    const message =
      error.response?.data?.detail ||
      error.response?.data?.message ||
      error.message ||
      "An unexpected error occurred";
    return Promise.reject(new Error(message));
  }
);

// ── Health ──────────────────────────────────────────────────────────────────

export async function checkHealth(): Promise<{ status: string }> {
  const res = await axios.get("/health");
  return res.data;
}

// ── Demo / E2E API ──────────────────────────────────────────────────────────

export async function startBuild(req: BuildRequest): Promise<BuildResultResponse> {
  const res = await api.post("/demo/build", req);
  return res.data;
}

export async function startBuildUpload(
  docFiles: File[],
  ddlFiles: File[],
  options?: {
    clear_graph?: boolean;
    study_id?: string;
    lazy_extraction?: boolean;
  }
): Promise<BuildResultResponse> {
  const form = new FormData();
  docFiles.forEach((f) => form.append("doc_files", f));
  ddlFiles.forEach((f) => form.append("ddl_files", f));
  if (options?.clear_graph !== undefined)
    form.append("clear_graph", String(options.clear_graph));
  if (options?.study_id) form.append("study_id", options.study_id);
  if (options?.lazy_extraction !== undefined)
    form.append("lazy_extraction", String(options.lazy_extraction));
  const res = await api.post("/demo/build/upload", form, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return res.data;
}

export async function getBuildStatus(jobId: string): Promise<BuildResultResponse> {
  const res = await api.get(`/demo/build/${jobId}`);
  return res.data;
}

export async function submitQuery(req: QueryRequest): Promise<QueryResponse> {
  const res = await api.post("/demo/query", req);
  return res.data;
}

export async function startPipeline(
  req: PipelineRequest
): Promise<PipelineJobResponse> {
  const res = await api.post("/demo/pipeline", req);
  return res.data;
}

export async function startPipelineUpload(
  docFiles: File[],
  ddlFiles: File[],
  questions: string[],
  options?: {
    clear_graph?: boolean;
    lazy_extraction?: boolean;
    run_ragas?: boolean;
    study_id?: string;
  }
): Promise<PipelineJobResponse> {
  const form = new FormData();
  docFiles.forEach((f) => form.append("doc_files", f));
  ddlFiles.forEach((f) => form.append("ddl_files", f));
  questions.forEach((q) => form.append("questions", q));
  if (options?.clear_graph !== undefined)
    form.append("clear_graph", String(options.clear_graph));
  if (options?.lazy_extraction !== undefined)
    form.append("lazy_extraction", String(options.lazy_extraction));
  if (options?.run_ragas !== undefined)
    form.append("run_ragas", String(options.run_ragas));
  if (options?.study_id) form.append("study_id", options.study_id);
  const res = await api.post("/demo/pipeline/upload", form, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return res.data;
}

export async function getPipelineStatus(
  jobId: string
): Promise<PipelineResultResponse> {
  const res = await api.get(`/demo/pipeline/${jobId}`);
  return res.data;
}

export async function getDemoJobs(): Promise<DemoJob[]> {
  const res = await api.get("/demo/jobs");
  return res.data;
}

export async function getGraphStats(): Promise<GraphStatsResponse> {
  const res = await api.get("/demo/graph/stats");
  return res.data;
}

export async function clearGraph(): Promise<{ nodes_deleted: number }> {
  const res = await api.delete("/demo/graph");
  return res.data;
}

export async function getGraphData(): Promise<GraphDataResponse> {
  const res = await api.get("/demo/graph/data");
  return res.data;
}

// ── Ablation API ────────────────────────────────────────────────────────────

export async function getAblationMatrix(): Promise<AblationMatrixEntry[]> {
  const res = await api.get("/ablation/matrix");
  return res.data;
}

export async function getAblationDatasets(): Promise<string[]> {
  const res = await api.get("/ablation/datasets");
  return res.data;
}

export async function startPresetAblation(
  req: PresetAblationRequest
): Promise<PresetAblationJobResponse> {
  const res = await api.post("/ablation/run/preset", req);
  return res.data;
}

export async function startCustomAblation(
  req: CustomAblationRequest
): Promise<AblationJobResponse> {
  const res = await api.post("/ablation/run/custom", req);
  return res.data;
}

export async function getAblationStatus(
  jobId: string
): Promise<AblationResultResponse> {
  const res = await api.get(`/ablation/status/${jobId}`);
  return res.data;
}

export async function getAblationJobs(): Promise<AblationJobResponse[]> {
  const res = await api.get("/ablation/jobs");
  return res.data;
}

export async function getEvaluationBundle(
  studyId: string,
  datasetId: string
): Promise<Record<string, unknown>> {
  const res = await api.get(`/ablation/bundle/${studyId}/${datasetId}`);
  return res.data;
}

export async function getAIJudgePayload(
  studyId: string,
  datasetId: string
): Promise<AIJudgePayload> {
  const res = await api.get(`/ablation/evaluate/${studyId}/${datasetId}`);
  return res.data;
}

// ── KG Snapshot API ─────────────────────────────────────────────────────────

export async function listKGSnapshots(): Promise<KGSnapshotMeta[]> {
  const res = await api.get("/demo/kg/snapshots");
  return res.data;
}

export async function getActiveKGSnapshot(): Promise<KGSnapshotMeta | null> {
  const res = await api.get("/demo/kg/snapshots/active");
  return res.data;
}

export async function saveKGSnapshot(req: SaveSnapshotRequest): Promise<KGSnapshotMeta> {
  const res = await api.post("/demo/kg/snapshots", req);
  return res.data;
}

export async function loadKGSnapshot(snapshotId: string): Promise<KGSnapshotMeta> {
  const res = await api.post(`/demo/kg/snapshots/${snapshotId}/load`);
  return res.data;
}

export async function ejectKGSnapshot(): Promise<void> {
  await api.post("/demo/kg/snapshots/eject");
}

export async function deleteKGSnapshot(snapshotId: string): Promise<void> {
  await api.delete(`/demo/kg/snapshots/${snapshotId}`);
}
