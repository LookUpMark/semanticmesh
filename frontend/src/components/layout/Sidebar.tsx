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
  { to: "/", icon: LayoutDashboard, label: "Dashboard" },
  { to: "/build", icon: Hammer, label: "KG Builder" },
  { to: "/query", icon: MessageSquare, label: "Query" },
  { to: "/graph", icon: Network, label: "Graph" },
  { to: "/ablation", icon: FlaskConical, label: "Ablation" },
  { to: "/settings", icon: Settings, label: "Settings" },
];

export function Sidebar() {
  return (
    <aside className="flex w-56 shrink-0 flex-col border-r border-border bg-card">
      <div className="flex h-14 items-center gap-2 border-b border-border px-4">
        <Database className="size-5 text-primary" />
        <span className="text-sm font-semibold tracking-tight">
          GraphRAG Studio
        </span>
      </div>

      <nav className="flex flex-1 flex-col gap-1 p-2">
        {NAV_ITEMS.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            end={item.to === "/"}
            className={({ isActive }) =>
              cn(
                "flex items-center gap-2.5 rounded-md px-3 py-2 text-sm font-medium transition-colors",
                isActive
                  ? "bg-primary text-primary-foreground"
                  : "text-muted-foreground hover:bg-muted hover:text-foreground"
              )
            }
          >
            <item.icon className="size-4" />
            {item.label}
          </NavLink>
        ))}
      </nav>

      <div className="border-t border-border p-3">
        <p className="text-[11px] text-muted-foreground">
          Multi-Agent GraphRAG
        </p>
      </div>
    </aside>
  );
}
