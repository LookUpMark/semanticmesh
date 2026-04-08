import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useEffect, useRef, useState } from "react";
import {
  getDemoJobs,
  getBuildStatus,
  getPipelineStatus,
  startBuildUpload,
  startPipelineUpload,
  submitQuery,
} from "@/lib/api";
import type { BuildResultResponse, QueryRequest } from "@/types/api";
import { toast } from "sonner";

export function useDemoJobs() {
  return useQuery({
    queryKey: ["demoJobs"],
    queryFn: getDemoJobs,
    refetchInterval: 30_000,  // reduced: job list doesn’t need frequent polling
  });
}

/**
 * SSE-based build status hook. Opens an EventSource to /api/v1/demo/build/{id}/stream
 * and updates state on each server push. Falls back gracefully to polling if SSE fails.
 */
export function useBuildStatus(jobId: string | null) {
  const [data, setData] = useState<BuildResultResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const esRef = useRef<EventSource | null>(null);
  const queryClient = useQueryClient();

  useEffect(() => {
    if (!jobId) return;

    // If already terminal, fetch once via REST and stop
    if (data?.status === "done" || data?.status === "failed") return;

    const es = new EventSource(`/api/v1/demo/build/${jobId}/stream`);
    esRef.current = es;

    es.onmessage = (event) => {
      try {
        const payload: BuildResultResponse = JSON.parse(event.data);
        setData(payload);
        if (payload.status === "done" || payload.status === "failed") {
          es.close();
          queryClient.invalidateQueries({ queryKey: ["demoJobs"] });
        }
      } catch {
        // ignore malformed frames
      }
    };

    es.onerror = () => {
      es.close();
      // Fallback: fetch current status once via REST
      getBuildStatus(jobId)
        .then(setData)
        .catch((e) => setError(String(e)));
    };

    return () => {
      es.close();
    };
  }, [jobId]); // eslint-disable-line react-hooks/exhaustive-deps

  return { data, error, isLoading: !data && !error };
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
