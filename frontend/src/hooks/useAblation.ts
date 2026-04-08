import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  getAblationMatrix,
  getAblationDatasets,
  getAblationStatus,
  getAblationJobs,
  startPresetAblation,
  startCustomAblation,
  getAIJudgePayload,
} from "@/lib/api";
import type { PresetAblationRequest, CustomAblationRequest } from "@/types/api";
import { toast } from "sonner";

export function useAblationMatrix() {
  return useQuery({
    queryKey: ["ablationMatrix"],
    queryFn: getAblationMatrix,
  });
}

export function useAblationDatasets() {
  return useQuery({
    queryKey: ["ablationDatasets"],
    queryFn: getAblationDatasets,
  });
}

export function useAblationJobs() {
  return useQuery({
    queryKey: ["ablationJobs"],
    queryFn: getAblationJobs,
    refetchInterval: 5_000,
  });
}

export function useAblationStatus(jobId: string | null) {
  return useQuery({
    queryKey: ["ablationStatus", jobId],
    queryFn: () => getAblationStatus(jobId!),
    enabled: !!jobId,
    refetchInterval: (query) => {
      const status = query.state.data?.status;
      if (status === "done" || status === "failed") return false;
      return 3_000;
    },
  });
}

export function useRunPresetAblation() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (req: PresetAblationRequest) => startPresetAblation(req),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["ablationJobs"] });
      toast.success("Preset ablation job queued");
    },
    onError: (err: Error) => {
      toast.error("Ablation failed: " + err.message);
    },
  });
}

export function useRunCustomAblation() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (req: CustomAblationRequest) => startCustomAblation(req),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["ablationJobs"] });
      toast.success("Custom ablation job queued");
    },
    onError: (err: Error) => {
      toast.error("Ablation failed: " + err.message);
    },
  });
}

export function useAIJudgePayload(studyId: string | null, datasetId: string | null) {
  return useQuery({
    queryKey: ["aiJudgePayload", studyId, datasetId],
    queryFn: () => getAIJudgePayload(studyId!, datasetId!),
    enabled: !!studyId && !!datasetId,
  });
}
