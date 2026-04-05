import { Outlet } from "react-router-dom";
import { Sidebar } from "./Sidebar";
import { Toaster } from "sonner";

export function AppLayout() {
  return (
    <div className="flex h-screen overflow-hidden bg-background text-foreground">
      <Sidebar />
      <main className="flex-1 overflow-y-auto">
        <Outlet />
      </main>
      <Toaster richColors position="top-right" />
    </div>
  );
}
