import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  listConversations,
  getConversation,
  saveConversation,
  renameConversation,
  deleteConversation,
} from "@/lib/api";
import type { SaveConversationRequest, RenameConversationRequest } from "@/types/api";
import { toast } from "sonner";

export function useConversations() {
  return useQuery({
    queryKey: ["conversations"],
    queryFn: listConversations,
    staleTime: 15_000,
  });
}

export function useConversationDetail(id: string | null) {
  return useQuery({
    queryKey: ["conversation", id],
    queryFn: () => getConversation(id!),
    enabled: !!id,
    staleTime: 30_000,
  });
}

export function useSaveConversation() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (req: SaveConversationRequest) => saveConversation(req),
    onSuccess: (conv) => {
      qc.invalidateQueries({ queryKey: ["conversations"] });
      toast.success(`Conversation "${conv.title}" saved`);
    },
    onError: (err: Error) => toast.error("Save failed: " + err.message),
  });
}

export function useRenameConversation() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, req }: { id: string; req: RenameConversationRequest }) =>
      renameConversation(id, req),
    onSuccess: (conv) => {
      qc.invalidateQueries({ queryKey: ["conversations"] });
      qc.invalidateQueries({ queryKey: ["conversation", conv.id] });
      toast.success(`Renamed to "${conv.title}"`);
    },
    onError: (err: Error) => toast.error("Rename failed: " + err.message),
  });
}

export function useDeleteConversation() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => deleteConversation(id),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["conversations"] });
      toast.success("Conversation deleted");
    },
    onError: (err: Error) => toast.error("Delete failed: " + err.message),
  });
}
