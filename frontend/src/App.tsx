import { useEffect } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { Toaster } from "sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { AppLayout } from "@/components/layout/AppLayout";
import { DashboardPage } from "@/pages/DashboardPage";
import { KGBuilderPage } from "@/pages/KGBuilderPage";
import { QueryPage } from "@/pages/QueryPage";
import { GraphVisualizationPage } from "@/pages/GraphVisualizationPage";
import { AblationPage } from "@/pages/AblationPage";
import { SettingsPage } from "@/pages/SettingsPage";
import { SettingsProvider } from "@/contexts/SettingsContext";

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
        <TooltipProvider>
          <Toaster position="top-right" richColors />
          <BrowserRouter>
            <Routes>
              <Route element={<AppLayout />}>
                <Route index element={<DashboardPage />} />
                <Route path="/build" element={<KGBuilderPage />} />
                <Route path="/query" element={<QueryPage />} />
                <Route path="/graph" element={<GraphVisualizationPage />} />
                <Route path="/ablation" element={<AblationPage />} />
                <Route path="/settings" element={<SettingsPage />} />
              </Route>
            </Routes>
          </BrowserRouter>
        </TooltipProvider>
      </SettingsProvider>
    </QueryClientProvider>
  );
}
