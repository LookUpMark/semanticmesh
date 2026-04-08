import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AppLayout } from "@/components/layout/AppLayout";
import { DashboardPage } from "@/pages/DashboardPage";
import { KGBuilderPage } from "@/pages/KGBuilderPage";
import { QueryPage } from "@/pages/QueryPage";
import { GraphVisualizationPage } from "@/pages/GraphVisualizationPage";
import { AblationPage } from "@/pages/AblationPage";
import { SettingsPage } from "@/pages/SettingsPage";

export function AppRouter() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<AppLayout />}>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/build" element={<KGBuilderPage />} />
          <Route path="/query" element={<QueryPage />} />
          <Route path="/graph" element={<GraphVisualizationPage />} />
          <Route path="/ablation" element={<AblationPage />} />
          <Route path="/settings" element={<SettingsPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
