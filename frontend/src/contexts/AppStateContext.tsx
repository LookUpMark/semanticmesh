/**
 * AppStateContext — global UI state that persists across route changes.
 *
 * Stores:
 *  - Query page chat messages (so the conversation survives navigation)
 *  - Active KG build job ID (so the progress card survives navigation)
 */

import {
  createContext,
  useContext,
  useState,
  useCallback,
  type Dispatch,
  type ReactNode,
  type SetStateAction,
} from "react";

import type { QueryResponse } from "@/types/api";

// ── Chat message type (used by QueryPage) ─────────────────────────────────

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
  metadata?: QueryResponse;
  isLoading?: boolean;
}

// ── Context shape ─────────────────────────────────────────────────────────

interface AppState {
  // Query page
  queryMessages: ChatMessage[];
  setQueryMessages: Dispatch<SetStateAction<ChatMessage[]>>;
  clearQueryMessages: () => void;

  // KG Builder page
  activeBuildJobId: string | null;
  setActiveBuildJobId: (id: string | null) => void;
}

const AppStateContext = createContext<AppState | null>(null);

// ── Provider ──────────────────────────────────────────────────────────────

export function AppStateProvider({ children }: { children: ReactNode }) {
  const [queryMessages, setQueryMessages] = useState<ChatMessage[]>([]);

  // Persist job ID in sessionStorage so a hard-reload on the same tab shows it
  const [activeBuildJobId, setActiveBuildJobIdState] = useState<string | null>(
    () => sessionStorage.getItem("active_build_job_id"),
  );

  const setActiveBuildJobId = useCallback((id: string | null) => {
    setActiveBuildJobIdState(id);
    if (id) {
      sessionStorage.setItem("active_build_job_id", id);
    } else {
      sessionStorage.removeItem("active_build_job_id");
    }
  }, []);

  const clearQueryMessages = useCallback(() => setQueryMessages([]), []);

  return (
    <AppStateContext.Provider
      value={{
        queryMessages,
        setQueryMessages,
        clearQueryMessages,
        activeBuildJobId,
        setActiveBuildJobId,
      }}
    >
      {children}
    </AppStateContext.Provider>
  );
}

// ── Hook ──────────────────────────────────────────────────────────────────

export function useAppState(): AppState {
  const ctx = useContext(AppStateContext);
  if (!ctx) {
    throw new Error("useAppState must be used within AppStateProvider");
  }
  return ctx;
}
