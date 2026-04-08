import { NavLink } from "react-router-dom";
import {
  LayoutDashboard,
  Hammer,
  MessageSquare,
  Network,
  FlaskConical,
  Settings,
  Database,
} from "lucide-react";
import { cn } from "@/lib/utils";

const NAV_ITEMS = [
  { to: "/", icon: LayoutDashboard, label: "Dashboard", description: "Overview & pipeline jobs" },
  { to: "/build", icon: Hammer, label: "KG Builder", description: "Build the Knowledge Graph" },
  { to: "/query", icon: MessageSquare, label: "Query", description: "Ask questions to your KG" },
  { to: "/graph", icon: Network, label: "Graph", description: "Visualise graph structure" },
  { to: "/ablation", icon: FlaskConical, label: "Ablation", description: "Run ablation studies" },
  { to: "/settings", icon: Settings, label: "Settings", description: "Configure the pipeline" },
];

export function Sidebar({ onNavigate }: { onNavigate?: () => void } = {}) {
  return (
    <aside className="flex w-56 shrink-0 flex-col border-r border-sidebar-border bg-sidebar">
      {/* Logo */}
      <div className="flex h-14 items-center gap-2.5 border-b border-sidebar-border px-4">
        <div className="flex size-7 items-center justify-center rounded-md bg-primary/15">
          <Database className="size-4 text-primary" />
        </div>
        <div className="flex flex-col leading-none">
          <span className="text-sm font-semibold tracking-tight text-sidebar-foreground">
            GraphRAG
          </span>
          <span className="text-[10px] text-muted-foreground">Studio</span>
        </div>
      </div>

      {/* Nav */}
      <nav className="flex flex-1 flex-col gap-0.5 p-2">
        {NAV_ITEMS.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            end={item.to === "/"}
            onClick={onNavigate}
            title={item.description}
            className={({ isActive }) =>
              cn(
                "flex items-center gap-2.5 rounded-md px-3 py-2 text-sm font-medium transition-colors",
                isActive
                  ? "bg-primary/15 text-primary"
                  : "text-muted-foreground hover:bg-sidebar-accent hover:text-sidebar-foreground"
              )
            }
          >
            <item.icon className="size-4 shrink-0" />
            {item.label}
          </NavLink>
        ))}
      </nav>

      {/* Footer */}
      <div className="border-t border-sidebar-border p-3 space-y-0.5">
        <p className="text-[11px] font-medium text-muted-foreground">
          Multi-Agent Framework
        </p>
        <p className="text-[10px] text-muted-foreground/60">
          Semantic Discovery & GraphRAG
        </p>
      </div>
    </aside>
  );
}

