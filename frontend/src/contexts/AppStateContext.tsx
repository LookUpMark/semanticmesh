/**
 * AppStateContext — global UI state that persists across route changes.
 *
 * Stores:
 *  - Query page chat messages (persisted to localStorage per session)
 *  - Session ID (UUID, persisted to localStorage — ties multi-turn history to backend)
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

// ── localStorage helpers ──────────────────────────────────────────────────

const SESSION_ID_KEY = "thesis_session_id";
const CHAT_HISTORY_KEY = "thesis_chat_history";
const MAX_PERSISTED_MESSAGES = 100;

function generateSessionId(): string {
  return crypto.randomUUID();
}

function loadSessionId(): string {
  const stored = localStorage.getItem(SESSION_ID_KEY);
  if (stored) return stored;
  const id = generateSessionId();
  localStorage.setItem(SESSION_ID_KEY, id);
  return id;
}

function loadMessages(): ChatMessage[] {
  try {
    const raw = localStorage.getItem(CHAT_HISTORY_KEY);
    if (!raw) return [];
    const parsed: ChatMessage[] = JSON.parse(raw);
    // Drop loading placeholders that survived a crash
    return parsed.filter((m) => !m.isLoading);
  } catch {
    return [];
  }
}

function saveMessages(msgs: ChatMessage[]): void {
  try {
    // Only persist real (non-loading) messages, capped to avoid quota issues
    const toSave = msgs
      .filter((m) => !m.isLoading)
      .slice(-MAX_PERSISTED_MESSAGES);
    localStorage.setItem(CHAT_HISTORY_KEY, JSON.stringify(toSave));
  } catch {
    // Quota exceeded or serialisation error — degrade gracefully
  }
}

// ── Context shape ─────────────────────────────────────────────────────────

interface AppState {
  // Query page
  queryMessages: ChatMessage[];
  setQueryMessages: Dispatch<SetStateAction<ChatMessage[]>>;
  clearQueryMessages: () => void;
  sessionId: string;
  resetSession: () => void;

  // KG Builder page
  activeBuildJobId: string | null;
  setActiveBuildJobId: (id: string | null) => void;
}

const AppStateContext = createContext<AppState | null>(null);

// ── Provider ──────────────────────────────────────────────────────────────

export function AppStateProvider({ children }: { children: ReactNode }) {
  const [sessionId, setSessionId] = useState<string>(() => loadSessionId());
  const [queryMessages, setQueryMessagesRaw] = useState<ChatMessage[]>(() =>
    loadMessages(),
  );

  // Wrap setter so every update is also persisted to localStorage
  const setQueryMessages: Dispatch<SetStateAction<ChatMessage[]>> = useCallback(
    (action) => {
      setQueryMessagesRaw((prev) => {
        const next =
          typeof action === "function" ? action(prev) : action;
        saveMessages(next);
        return next;
      });
    },
    [],
  );

  const clearQueryMessages = useCallback(() => {
    setQueryMessagesRaw([]);
    localStorage.removeItem(CHAT_HISTORY_KEY);
  }, []);

  /** Start a fresh conversation with a new session ID. */
  const resetSession = useCallback(() => {
    const id = generateSessionId();
    localStorage.setItem(SESSION_ID_KEY, id);
    setSessionId(id);
    setQueryMessagesRaw([]);
    localStorage.removeItem(CHAT_HISTORY_KEY);
  }, []);

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

  return (
    <AppStateContext.Provider
      value={{
        queryMessages,
        setQueryMessages,
        clearQueryMessages,
        sessionId,
        resetSession,
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
