import { useState } from "react";
import { Outlet } from "react-router-dom";
import { Menu, Database } from "lucide-react";
import { Sidebar } from "./Sidebar";
import { Toaster } from "sonner";
import { Sheet, SheetContent } from "@/components/ui/sheet";
import { Button } from "@/components/ui/button";

export function AppLayout() {
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <div className="flex h-screen overflow-hidden bg-background text-foreground">
      {/* Desktop sidebar — hidden below md */}
      <div className="hidden md:flex">
        <Sidebar />
      </div>

      {/* Content area */}
      <div className="flex flex-1 flex-col overflow-hidden">
        {/* Mobile top bar — visible below md */}
        <header className="flex h-14 items-center gap-3 border-b border-border px-4 md:hidden">
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setMobileOpen(true)}
            aria-label="Open navigation"
          >
            <Menu className="size-5" />
          </Button>
          <div className="flex items-center gap-2">
            <div className="flex size-6 items-center justify-center rounded bg-primary/15">
              <Database className="size-3.5 text-primary" />
            </div>
            <span className="text-sm font-semibold">GraphRAG Studio</span>
          </div>
        </header>

        <main className="flex-1 overflow-y-auto">
          <Outlet />
        </main>
      </div>

      {/* Mobile sidebar drawer */}
      <Sheet open={mobileOpen} onOpenChange={setMobileOpen}>
        <SheetContent side="left" className="w-56 p-0">
          <Sidebar onNavigate={() => setMobileOpen(false)} />
        </SheetContent>
      </Sheet>

      <Toaster richColors position="top-right" />
    </div>
  );
}
