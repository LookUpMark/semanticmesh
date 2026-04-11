/**
 * ConversationSidebar — list, save, rename, delete, and load saved conversations.
 */

import { useState } from "react";
import {
  MessageSquare,
  Plus,
  Pencil,
  Trash2,
  Check,
  X,
  Loader2,
  BookOpen,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Badge } from "@/components/ui/badge";
import {
  useConversations,
  useSaveConversation,
  useRenameConversation,
  useDeleteConversation,
} from "@/hooks/useConversations";
import { getConversation } from "@/lib/api";
import type { ConversationMeta, ConversationMessage } from "@/types/api";

interface Props {
  /** Current session ID (used when saving the active conversation). */
  sessionId: string;
  /** Current messages in the active chat. */
  currentMessages: ConversationMessage[];
  /** ID of the currently loaded KG snapshot (if any). */
  activeSnapshotId?: string | null;
  /** Called when user clicks a saved conversation to load it. */
  onLoad: (conv: { sessionId: string; messages: ConversationMessage[] }) => void;
  /** Called when user starts a new conversation. */
  onNew: () => void;
}

export function ConversationSidebar({
  sessionId,
  currentMessages,
  activeSnapshotId,
  onLoad,
  onNew,
}: Props) {
  const { data: conversations = [], isLoading } = useConversations();
  const saveConv = useSaveConversation();
  const renameConv = useRenameConversation();
  const deleteConv = useDeleteConversation();

  const [renamingId, setRenamingId] = useState<string | null>(null);
  const [renameValue, setRenameValue] = useState("");
  const [savingTitle, setSavingTitle] = useState("");
  const [showSaveInput, setShowSaveInput] = useState(false);
  const [loadingId, setLoadingId] = useState<string | null>(null);

  const handleSave = () => {
    if (!currentMessages.length) return;
    saveConv.mutate(
      {
        session_id: sessionId,
        title: savingTitle.trim(),
        messages: currentMessages,
        active_snapshot_id: activeSnapshotId ?? null,
      },
      {
        onSuccess: () => {
          setSavingTitle("");
          setShowSaveInput(false);
        },
      }
    );
  };

  const handleRename = (conv: ConversationMeta) => {
    if (!renameValue.trim()) {
      setRenamingId(null);
      return;
    }
    renameConv.mutate(
      { id: conv.id, req: { title: renameValue.trim() } },
      { onSuccess: () => setRenamingId(null) }
    );
  };

  const nonLoadingMessages = currentMessages.filter((m) => !("isLoading" in m && (m as { isLoading?: boolean }).isLoading));
  const hasMessages = nonLoadingMessages.length > 0;

  return (
    <div className="flex flex-col h-full w-64 border-r border-border bg-muted/20">
      {/* Header */}
      <div className="px-3 py-3 border-b border-border">
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center gap-1.5">
            <BookOpen className="size-3.5 text-muted-foreground" />
            <span className="text-xs font-semibold">Conversations</span>
          </div>
          <Button
            variant="ghost"
            size="sm"
            className="h-6 w-6 p-0"
            onClick={onNew}
            title="New conversation"
          >
            <Plus className="size-3.5" />
          </Button>
        </div>

        {/* Save current conversation */}
        {hasMessages && (
          <div>
            {showSaveInput ? (
              <div className="flex items-center gap-1">
                <Input
                  className="h-6 text-xs flex-1 px-2"
                  placeholder="Title (optional)…"
                  value={savingTitle}
                  onChange={(e) => setSavingTitle(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === "Enter") handleSave();
                    if (e.key === "Escape") setShowSaveInput(false);
                  }}
                  autoFocus
                />
                <button
                  onClick={handleSave}
                  disabled={saveConv.isPending}
                  className="text-emerald-500 hover:text-emerald-400 disabled:opacity-50"
                >
                  {saveConv.isPending ? (
                    <Loader2 className="size-3.5 animate-spin" />
                  ) : (
                    <Check className="size-3.5" />
                  )}
                </button>
                <button
                  onClick={() => setShowSaveInput(false)}
                  className="text-muted-foreground hover:text-foreground"
                >
                  <X className="size-3.5" />
                </button>
              </div>
            ) : (
              <Button
                variant="outline"
                size="sm"
                className="w-full h-6 text-xs gap-1.5"
                onClick={() => setShowSaveInput(true)}
              >
                <Plus className="size-3" />
                Save current
              </Button>
            )}
          </div>
        )}
      </div>

      {/* Conversation list */}
      <ScrollArea className="flex-1">
        {isLoading ? (
          <div className="flex items-center justify-center py-8">
            <Loader2 className="size-4 animate-spin text-muted-foreground" />
          </div>
        ) : conversations.length === 0 ? (
          <p className="px-3 py-6 text-xs text-center text-muted-foreground">
            No saved conversations yet.
          </p>
        ) : (
          <div className="divide-y divide-border">
            {conversations.map((conv: ConversationMeta) => (
              <div
                key={conv.id}
                className="px-3 py-2.5 hover:bg-muted/40 group"
              >
                {renamingId === conv.id ? (
                  <div className="flex items-center gap-1">
                    <Input
                      className="h-6 text-xs flex-1 px-2"
                      value={renameValue}
                      onChange={(e) => setRenameValue(e.target.value)}
                      onKeyDown={(e) => {
                        if (e.key === "Enter") handleRename(conv);
                        if (e.key === "Escape") setRenamingId(null);
                      }}
                      autoFocus
                    />
                    <button
                      onClick={() => handleRename(conv)}
                      className="text-emerald-500 hover:text-emerald-400"
                    >
                      <Check className="size-3.5" />
                    </button>
                    <button
                      onClick={() => setRenamingId(null)}
                      className="text-muted-foreground"
                    >
                      <X className="size-3.5" />
                    </button>
                  </div>
                ) : (
                  <>
                    <button
                      className="w-full text-left"
                      disabled={loadingId === conv.id}
                      onClick={async () => {
                        setLoadingId(conv.id);
                        try {
                          const detail = await getConversation(conv.id);
                          onLoad({ sessionId: detail.session_id, messages: detail.messages });
                        } finally {
                          setLoadingId(null);
                        }
                      }}
                    >
                      <div className="flex items-start gap-1.5">
                        {loadingId === conv.id ? (
                          <Loader2 className="size-3 mt-0.5 shrink-0 animate-spin text-muted-foreground" />
                        ) : (
                          <MessageSquare className="size-3 mt-0.5 shrink-0 text-muted-foreground" />
                        )}
                        <span className="text-xs font-medium line-clamp-2 leading-tight">
                          {conv.title || conv.preview}
                        </span>
                      </div>
                      <div className="mt-1 flex items-center gap-2 pl-4">
                        <span className="text-[10px] text-muted-foreground">
                          {conv.message_count} msgs ·{" "}
                          {new Date(conv.updated_at).toLocaleDateString()}
                        </span>
                        {conv.active_snapshot_id && (
                          <Badge
                            variant="outline"
                            className="text-[9px] h-3.5 px-1"
                          >
                            KG
                          </Badge>
                        )}
                      </div>
                    </button>
                    <div className="flex items-center gap-0.5 mt-1 pl-4 opacity-0 group-hover:opacity-100 transition-opacity">
                      <button
                        onClick={() => {
                          setRenamingId(conv.id);
                          setRenameValue(conv.title || conv.preview);
                        }}
                        className="p-0.5 text-muted-foreground hover:text-foreground rounded"
                        title="Rename"
                      >
                        <Pencil className="size-3" />
                      </button>
                      <button
                        onClick={() => deleteConv.mutate(conv.id)}
                        className="p-0.5 text-muted-foreground hover:text-destructive rounded"
                        title="Delete"
                        disabled={deleteConv.isPending}
                      >
                        <Trash2 className="size-3" />
                      </button>
                    </div>
                  </>
                )}
              </div>
            ))}
          </div>
        )}
      </ScrollArea>
    </div>
  );
}
