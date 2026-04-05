import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  getDemoJobs,
  getBuildStatus,
  getPipelineStatus,
  startBuildUpload,
  startPipelineUpload,
  submitQuery,
} from "@/lib/api";
import type { QueryRequest } from "@/types/api";
import { toast } from "sonner";

export function useDemoJobs() {
  return useQuery({
    queryKey: ["demoJobs"],
    queryFn: getDemoJobs,
    refetchInterval: 5_000,
  });
}

export function useBuildStatus(jobId: string | null) {
  return useQuery({
    queryKey: ["buildStatus", jobId],
    queryFn: () => getBuildStatus(jobId!),
    enabled: !!jobId,
    refetchInterval: (query) => {
      const status = query.state.data?.status;
      if (status === "done" || status === "failed") return false;
      return 2_000;
    },
  });
}

export function useStartBuildUpload() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (params: { docFiles: File[]; ddlFiles: File[]; options?: { clear_graph?: boolean; study_id?: string; lazy_extraction?: boolean } }) =>
      startBuildUpload(params.docFiles, params.ddlFiles, params.options),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["demoJobs"] });
      toast.success("Build job queued");
    },
    onError: (err: Error) => {
      toast.error("Build failed: " + err.message);
    },
  });
}

export function usePipelineStatus(jobId: string | null) {
  return useQuery({
    queryKey: ["pipelineStatus", jobId],
    queryFn: () => getPipelineStatus(jobId!),
    enabled: !!jobId,
    refetchInterval: (query) => {
      const status = query.state.data?.status;
      if (status === "done" || status === "failed") return false;
      return 3_000;
    },
  });
}

export function useStartPipelineUpload() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (params: { docFiles: File[]; ddlFiles: File[]; questions: string[]; options?: { clear_graph?: boolean; lazy_extraction?: boolean; run_ragas?: boolean; study_id?: string } }) =>
      startPipelineUpload(params.docFiles, params.ddlFiles, params.questions, params.options),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["demoJobs"] });
      toast.success("Pipeline job queued");
    },
    onError: (err: Error) => {
      toast.error("Pipeline failed: " + err.message);
    },
  });
}

export function useSubmitQuery() {
  return useMutation({
    mutationFn: (req: QueryRequest) => submitQuery(req),
    onError: (err: Error) => {
      toast.error("Query failed: " + err.message);
    },
  });
}

export function useHealth() {
  return useQuery({
    queryKey: ["health"],
    queryFn: async () => {
      try {
        const res = await fetch("/health");
        const data = await res.json();
        return data as { status: string };
      } catch {
        return { status: "unhealthy" };
      }
    },
    refetchInterval: 30_000,
  });
}
