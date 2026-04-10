import { useEffect } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { Toaster } from "sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { AppLayout } from "@/components/layout/AppLayout";
import { ErrorBoundary } from "@/components/ErrorBoundary";
import { DashboardPage } from "@/pages/DashboardPage";
import { KGBuilderPage } from "@/pages/KGBuilderPage";
import { QueryPage } from "@/pages/QueryPage";
import { GraphVisualizationPage } from "@/pages/GraphVisualizationPage";
import { AblationPage } from "@/pages/AblationPage";
import { SettingsPage } from "@/pages/SettingsPage";
import { SettingsProvider } from "@/contexts/SettingsContext";
import { AppStateProvider } from "@/contexts/AppStateContext";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60,
      retry: 1,
    },
  },
});

function DarkModeInitializer() {
  useEffect(() => {
    document.documentElement.classList.add("dark");
  }, []);
  return null;
}

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <DarkModeInitializer />
      <SettingsProvider>
        <AppStateProvider>
        <TooltipProvider>
          <Toaster position="top-right" richColors />
          <BrowserRouter>
            <Routes>
              <Route element={<AppLayout />}>
                <Route index element={<ErrorBoundary><DashboardPage /></ErrorBoundary>} />
                <Route path="/build" element={<ErrorBoundary><KGBuilderPage /></ErrorBoundary>} />
                <Route path="/query" element={<ErrorBoundary><QueryPage /></ErrorBoundary>} />
                <Route path="/graph" element={<ErrorBoundary><GraphVisualizationPage /></ErrorBoundary>} />
                <Route path="/ablation" element={<ErrorBoundary><AblationPage /></ErrorBoundary>} />
                <Route path="/settings" element={<ErrorBoundary><SettingsPage /></ErrorBoundary>} />
              </Route>
            </Routes>
          </BrowserRouter>
        </TooltipProvider>
        </AppStateProvider>
      </SettingsProvider>
    </QueryClientProvider>
  );
}
