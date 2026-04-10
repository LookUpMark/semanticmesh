import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  listKGSnapshots,
  getActiveKGSnapshot,
  saveKGSnapshot,
  loadKGSnapshot,
  ejectKGSnapshot,
  deleteKGSnapshot,
} from "@/lib/api";
import type { SaveSnapshotRequest } from "@/types/api";
import { toast } from "sonner";

export function useKGSnapshots() {
  return useQuery({
    queryKey: ["kgSnapshots"],
    queryFn: listKGSnapshots,
    staleTime: 10_000,
  });
}

export function useActiveKGSnapshot() {
  return useQuery({
    queryKey: ["kgActiveSnapshot"],
    queryFn: getActiveKGSnapshot,
    staleTime: 10_000,
  });
}

export function useSaveKGSnapshot() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (req: SaveSnapshotRequest) => saveKGSnapshot(req),
    onSuccess: (snap) => {
      qc.invalidateQueries({ queryKey: ["kgSnapshots"] });
      toast.success(`Snapshot "${snap.name}" saved`, {
        description: `${snap.node_count} nodes · ${snap.edge_count} edges`,
      });
    },
    onError: (err: Error) => toast.error("Save failed: " + err.message),
  });
}

export function useLoadKGSnapshot() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (snapshotId: string) => loadKGSnapshot(snapshotId),
    onSuccess: (snap) => {
      qc.invalidateQueries({ queryKey: ["kgSnapshots"] });
      qc.invalidateQueries({ queryKey: ["kgActiveSnapshot"] });
      qc.invalidateQueries({ queryKey: ["graphStats"] });
      toast.success(`Knowledge Graph "${snap.name}" loaded`, {
        description: `${snap.node_count} nodes · ${snap.edge_count} edges restored`,
      });
    },
    onError: (err: Error) => toast.error("Load failed: " + err.message),
  });
}

export function useEjectKGSnapshot() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ejectKGSnapshot,
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["kgSnapshots"] });
      qc.invalidateQueries({ queryKey: ["kgActiveSnapshot"] });
      toast.info("Knowledge Graph ejected");
    },
    onError: (err: Error) => toast.error("Eject failed: " + err.message),
  });
}

export function useDeleteKGSnapshot() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (snapshotId: string) => deleteKGSnapshot(snapshotId),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["kgSnapshots"] });
      qc.invalidateQueries({ queryKey: ["kgActiveSnapshot"] });
      toast.success("Snapshot deleted");
    },
    onError: (err: Error) => toast.error("Delete failed: " + err.message),
  });
}
