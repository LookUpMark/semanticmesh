/**
 * KGSnapshotManager — Reusable component for listing, loading, saving,
 * renaming, and deleting Knowledge Graph snapshots.
 *
 * Used on both QueryPage (compact bar) and GraphVisualizationPage (panel).
 */

import { useState } from "react";
import {
  Database,
  FolderOpen,
  Plus,
  LogOut,
  Loader2,
  X,
  Pencil,
  Check,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from "@/components/ui/dialog";
import {
  useKGSnapshots,
  useActiveKGSnapshot,
  useSaveKGSnapshot,
  useLoadKGSnapshot,
  useEjectKGSnapshot,
  useDeleteKGSnapshot,
  useRenameKGSnapshot,
} from "@/hooks/useKGSnapshots";
import type { KGSnapshotMeta } from "@/types/api";

interface Props {
  /** Compact bar mode (used in QueryPage header) vs. expanded panel (Graph page). */
  variant?: "bar" | "panel";
  /** Called after a snapshot is loaded (so parent can refresh the graph). */
  onLoad?: () => void;
}

export function KGSnapshotManager({ variant = "bar", onLoad }: Props) {
  const { data: active, isLoading: activeLoading } = useActiveKGSnapshot();
  const { data: snapshots = [] } = useKGSnapshots();
  const loadKG = useLoadKGSnapshot();
  const ejectKG = useEjectKGSnapshot();
  const saveKG = useSaveKGSnapshot();
  const deleteKG = useDeleteKGSnapshot();
  const renameKG = useRenameKGSnapshot();

  const [showList, setShowList] = useState(false);
  const [showSaveDialog, setShowSaveDialog] = useState(false);
  const [saveName, setSaveName] = useState("");
  const [saveDesc, setSaveDesc] = useState("");

  // Inline rename state
  const [renamingId, setRenamingId] = useState<string | null>(null);
  const [renameValue, setRenameValue] = useState("");

  const handleSave = () => {
    if (!saveName.trim()) return;
    saveKG.mutate(
      { name: saveName.trim(), description: saveDesc.trim() },
      {
        onSuccess: () => {
          setShowSaveDialog(false);
          setSaveName("");
          setSaveDesc("");
        },
      }
    );
  };

  const handleLoad = (snap: KGSnapshotMeta) => {
    loadKG.mutate(snap.id, {
      onSuccess: () => {
        setShowList(false);
        onLoad?.();
      },
    });
  };

  const handleRenameSubmit = (snap: KGSnapshotMeta) => {
    if (!renameValue.trim()) {
      setRenamingId(null);
      return;
    }
    renameKG.mutate(
      { id: snap.id, req: { name: renameValue.trim() } },
      { onSuccess: () => setRenamingId(null) }
    );
  };

  const startRename = (snap: KGSnapshotMeta) => {
    setRenamingId(snap.id);
    setRenameValue(snap.name);
  };

  // ── Active badge ─────────────────────────────────────────────────────────

  const activeBadge = activeLoading ? (
    <Loader2 className="size-3.5 animate-spin text-muted-foreground" />
  ) : active ? (
    <Badge variant="default" className="gap-1.5 text-xs font-medium">
      <span className="size-1.5 rounded-full bg-emerald-400 inline-block" />
      {active.name}
      <span className="text-[10px] opacity-70">
        {active.node_count}n · {active.edge_count}e
      </span>
    </Badge>
  ) : (
    <Badge variant="outline" className="text-xs text-muted-foreground">
      No KG loaded
    </Badge>
  );

  // ── Snapshot list ─────────────────────────────────────────────────────────

  const snapshotList = (
    <div className={variant === "panel" ? "" : "absolute top-[6.5rem] right-4 z-50 w-80 rounded-lg border border-border bg-card shadow-lg"}>
      {variant === "bar" && (
        <div className="flex items-center justify-between border-b border-border px-3 py-2">
          <span className="text-xs font-semibold">Saved Knowledge Graphs</span>
          <button onClick={() => setShowList(false)}>
            <X className="size-3.5 text-muted-foreground" />
          </button>
        </div>
      )}
      <ScrollArea className={variant === "panel" ? "h-full" : "max-h-64"}>
        {snapshots.length === 0 ? (
          <p className="px-3 py-4 text-xs text-center text-muted-foreground">
            No snapshots saved yet.
          </p>
        ) : (
          <div className="divide-y divide-border">
            {snapshots.map((snap: KGSnapshotMeta) => (
              <div
                key={snap.id}
                className="flex items-center gap-2 px-3 py-2.5 hover:bg-muted/40"
              >
                <div className="flex-1 min-w-0">
                  {renamingId === snap.id ? (
                    <div className="flex items-center gap-1">
                      <Input
                        className="h-6 text-xs px-2"
                        value={renameValue}
                        onChange={(e) => setRenameValue(e.target.value)}
                        onKeyDown={(e) => {
                          if (e.key === "Enter") handleRenameSubmit(snap);
                          if (e.key === "Escape") setRenamingId(null);
                        }}
                        autoFocus
                      />
                      <button
                        onClick={() => handleRenameSubmit(snap)}
                        className="text-emerald-500 hover:text-emerald-400"
                      >
                        <Check className="size-3.5" />
                      </button>
                      <button
                        onClick={() => setRenamingId(null)}
                        className="text-muted-foreground hover:text-foreground"
                      >
                        <X className="size-3.5" />
                      </button>
                    </div>
                  ) : (
                    <>
                      <div className="flex items-center gap-1.5">
                        <span className="text-xs font-medium truncate">{snap.name}</span>
                        {snap.is_active && (
                          <span className="size-1.5 rounded-full bg-emerald-400 shrink-0" />
                        )}
                      </div>
                      <p className="text-[10px] text-muted-foreground">
                        {snap.node_count}n · {snap.edge_count}e ·{" "}
                        {new Date(snap.created_at).toLocaleDateString()}
                      </p>
                    </>
                  )}
                </div>
                {renamingId !== snap.id && (
                  <div className="flex gap-1 shrink-0">
                    <Button
                      variant="outline"
                      size="sm"
                      className="h-6 text-[10px] px-2"
                      disabled={snap.is_active || loadKG.isPending}
                      onClick={() => handleLoad(snap)}
                    >
                      {loadKG.isPending ? (
                        <Loader2 className="size-3 animate-spin" />
                      ) : (
                        "Load"
                      )}
                    </Button>
                    <Button
                      variant="ghost"
                      size="sm"
                      className="h-6 w-6 p-0 text-muted-foreground hover:text-foreground"
                      onClick={() => startRename(snap)}
                      title="Rename"
                    >
                      <Pencil className="size-3" />
                    </Button>
                    <Button
                      variant="ghost"
                      size="sm"
                      className="h-6 w-6 p-0 text-destructive hover:text-destructive"
                      onClick={() => deleteKG.mutate(snap.id)}
                      disabled={deleteKG.isPending}
                      title="Delete"
                    >
                      <X className="size-3" />
                    </Button>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </ScrollArea>
    </div>
  );

  // ── Save dialog ───────────────────────────────────────────────────────────

  const saveDialog = (
    <Dialog open={showSaveDialog} onOpenChange={setShowSaveDialog}>
      <DialogContent className="max-w-sm">
        <DialogHeader>
          <DialogTitle>Save Knowledge Graph</DialogTitle>
        </DialogHeader>
        <div className="space-y-3">
          <div className="space-y-1">
            <Label htmlFor="kg-name" className="text-xs">
              Name *
            </Label>
            <Input
              id="kg-name"
              placeholder="E-Commerce v1"
              value={saveName}
              onChange={(e) => setSaveName(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSave()}
              autoFocus
            />
          </div>
          <div className="space-y-1">
            <Label htmlFor="kg-desc" className="text-xs">
              Description
            </Label>
            <Input
              id="kg-desc"
              placeholder="Optional notes about this KG…"
              value={saveDesc}
              onChange={(e) => setSaveDesc(e.target.value)}
            />
          </div>
        </div>
        <DialogFooter>
          <Button
            variant="outline"
            size="sm"
            onClick={() => setShowSaveDialog(false)}
          >
            Cancel
          </Button>
          <Button
            size="sm"
            disabled={!saveName.trim() || saveKG.isPending}
            onClick={handleSave}
          >
            {saveKG.isPending ? (
              <Loader2 className="size-4 animate-spin" />
            ) : (
              "Save"
            )}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );

  // ── Panel variant ─────────────────────────────────────────────────────────

  if (variant === "panel") {
    return (
      <div className="flex flex-col gap-3">
        <div className="flex items-center gap-2">
          <Database className="size-4 shrink-0 text-muted-foreground" />
          <span className="text-sm font-semibold">Knowledge Graph</span>
        </div>
        {activeBadge}
        <div className="flex gap-2 flex-wrap">
          <Button
            variant="outline"
            size="sm"
            className="gap-1.5 text-xs flex-1"
            onClick={() => setShowSaveDialog(true)}
          >
            <Plus className="size-3.5" />
            Save current
          </Button>
          {active && (
            <Button
              variant="outline"
              size="sm"
              className="gap-1 text-xs"
              onClick={() => ejectKG.mutate()}
              disabled={ejectKG.isPending}
            >
              <LogOut className="size-3.5" />
              Eject
            </Button>
          )}
        </div>
        <div>
          <p className="text-xs text-muted-foreground mb-2 font-medium">
            Saved snapshots
          </p>
          {snapshotList}
        </div>
        {saveDialog}
      </div>
    );
  }

  // ── Bar variant (default) ─────────────────────────────────────────────────

  return (
    <div className="border-b border-border bg-muted/30 px-6 py-2 flex items-center gap-3 relative">
      <Database className="size-3.5 shrink-0 text-muted-foreground" />
      <span className="text-xs text-muted-foreground font-medium">
        Knowledge Graph:
      </span>
      {activeBadge}

      <div className="ml-auto flex items-center gap-1.5">
        <Button
          variant="ghost"
          size="sm"
          className="h-7 gap-1.5 text-xs"
          onClick={() => setShowList((v) => !v)}
        >
          <FolderOpen className="size-3.5" />
          Load
        </Button>
        <Button
          variant="ghost"
          size="sm"
          className="h-7 gap-1.5 text-xs"
          onClick={() => setShowSaveDialog(true)}
        >
          <Plus className="size-3.5" />
          Save
        </Button>
        {active && (
          <Button
            variant="ghost"
            size="sm"
            className="h-7 gap-1 text-xs text-muted-foreground"
            onClick={() => ejectKG.mutate()}
            disabled={ejectKG.isPending}
          >
            <LogOut className="size-3.5" />
            Eject
          </Button>
        )}
      </div>

      {showList && snapshotList}
      {saveDialog}
    </div>
  );
}
