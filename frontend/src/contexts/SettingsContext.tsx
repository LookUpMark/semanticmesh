import {
  createContext,
  useContext,
  useState,
  useCallback,
  type ReactNode,
} from "react";

interface SettingsState {
  apiKey: string;
  apiBaseUrl: string;
  setApiKey: (key: string) => void;
  setApiBaseUrl: (url: string) => void;
}

const SettingsContext = createContext<SettingsState | null>(null);

export function SettingsProvider({ children }: { children: ReactNode }) {
  const [apiKey, setApiKeyState] = useState<string>(
    () => localStorage.getItem("thesis_api_key") || ""
  );
  const [apiBaseUrl, setApiBaseUrlState] = useState<string>(
    () => localStorage.getItem("thesis_api_base_url") || "/api/v1"
  );

  const setApiKey = useCallback((key: string) => {
    setApiKeyState(key);
    if (key) {
      localStorage.setItem("thesis_api_key", key);
    } else {
      localStorage.removeItem("thesis_api_key");
    }
  }, []);

  const setApiBaseUrl = useCallback((url: string) => {
    setApiBaseUrlState(url);
    localStorage.setItem("thesis_api_base_url", url);
  }, []);

  return (
    <SettingsContext.Provider
      value={{ apiKey, apiBaseUrl, setApiKey, setApiBaseUrl }}
    >
      {children}
    </SettingsContext.Provider>
  );
}

export function useSettings(): SettingsState {
  const ctx = useContext(SettingsContext);
  if (!ctx) {
    throw new Error("useSettings must be used within SettingsProvider");
  }
  return ctx;
}
