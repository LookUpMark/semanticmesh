import { Link } from "react-router-dom";
import {
  Network,
  ArrowLeftRight,
  Loader2,
  CheckCircle2,
  XCircle,
  Hammer,
  MessageSquare,
  FlaskConical,
  AlertTriangle,
} from "lucide-react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Skeleton } from "@/components/ui/skeleton";
import { useGraphStats } from "@/hooks/useGraphStats";
import { useDemoJobs, useHealth } from "@/hooks/useJobs";
import type { DemoJob } from "@/types/api";

function StatusIcon({ status }: { status: string }) {
  switch (status) {
    case "done":
      return <CheckCircle2 className="size-4 text-emerald-400" />;
    case "running":
      return <Loader2 className="size-4 animate-spin text-blue-400" />;
    case "failed":
      return <XCircle className="size-4 text-red-400" />;
    default:
      return <Loader2 className="size-4 animate-spin text-yellow-400" />;
  }
}

function StatusBadge({ status }: { status: string }) {
  const variantMap: Record<string, "default" | "secondary" | "destructive" | "outline"> = {
    done: "default",
    running: "secondary",
    failed: "destructive",
    queued: "outline",
  };
  return <Badge variant={variantMap[status] ?? "outline"}>{status}</Badge>;
}

function TypeBadge({ type }: { type: string }) {
  const iconMap: Record<string, typeof Hammer> = {
    build: Hammer,
    pipeline: FlaskConical,
    ablation: FlaskConical,
  };
  const Icon = iconMap[type] ?? Hammer;
  return (
    <Badge variant="outline" className="gap-1">
      <Icon className="size-3" />
      {type}
    </Badge>
  );
}

function StatCard({
  title,
  value,
  icon: Icon,
  description,
  loading,
}: {
  title: string;
  value: React.ReactNode;
  icon: React.ElementType;
  description?: string;
  loading?: boolean;
}) {
  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between pb-2">
        <CardTitle className="text-sm font-medium text-muted-foreground">
          {title}
        </CardTitle>
        <Icon className="size-4 text-muted-foreground" />
      </CardHeader>
      <CardContent>
        {loading ? (
          <Skeleton className="h-8 w-20" />
        ) : (
          <>
            <div className="text-2xl font-bold">{value}</div>
            {description && (
              <p className="text-xs text-muted-foreground">{description}</p>
            )}
          </>
        )}
      </CardContent>
    </Card>
  );
}

function RecentJobsTable({ jobs, loading }: { jobs: DemoJob[]; loading: boolean }) {
  if (loading) {
    return (
      <div className="space-y-3 p-4">
        {Array.from({ length: 3 }).map((_, i) => (
          <Skeleton key={i} className="h-10 w-full" />
        ))}
      </div>
    );
  }

  if (jobs.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-12 text-center">
        <AlertTriangle className="mb-2 size-8 text-muted-foreground" />
        <p className="text-sm text-muted-foreground">No jobs yet</p>
        <p className="text-xs text-muted-foreground">
          Start a build or pipeline to see jobs here.
        </p>
      </div>
    );
  }

  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>Type</TableHead>
          <TableHead>Status</TableHead>
          <TableHead>Job ID</TableHead>
          <TableHead>Study ID</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {jobs.map((job) => (
          <TableRow key={job.job_id}>
            <TableCell>
              <TypeBadge type={job.type} />
            </TableCell>
            <TableCell>
              <div className="flex items-center gap-1.5">
                <StatusIcon status={job.status} />
                <StatusBadge status={job.status} />
              </div>
            </TableCell>
            <TableCell className="font-mono text-xs">
              {job.job_id.slice(0, 8)}...
            </TableCell>
            <TableCell className="text-sm">{job.study_id}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
}

function GraphStatsGrid({
  stats,
  loading,
}: {
  stats: Record<string, number> | null;
  loading: boolean;
}) {
  const fields = [
    { key: "business_concepts", label: "Business Concepts" },
    { key: "physical_tables", label: "Physical Tables" },
    { key: "parent_chunks", label: "Parent Chunks" },
    { key: "child_chunks", label: "Child Chunks" },
    { key: "mentions_edges", label: "MENTIONS Edges" },
    { key: "maps_to_edges", label: "MAPS_TO Edges" },
  ];

  return (
    <div className="grid grid-cols-3 gap-3">
      {fields.map((f) => (
        <Card key={f.key} className="p-3">
          {loading ? (
            <Skeleton className="h-6 w-16" />
          ) : (
            <>
              <p className="text-xs text-muted-foreground">{f.label}</p>
              <p className="text-lg font-semibold">
                {stats?.[f.key]?.toLocaleString() ?? "-"}
              </p>
            </>
          )}
        </Card>
      ))}
    </div>
  );
}

export function DashboardPage() {
  const { data: graphStats, isLoading: statsLoading } = useGraphStats();
  const { data: jobs, isLoading: jobsLoading } = useDemoJobs();
  const { data: health } = useHealth();

  const systemOk = health?.status === "ok" || health?.status === "healthy";

  return (
    <div className="p-6 space-y-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight">Dashboard</h1>
        <p className="text-sm text-muted-foreground">
          Overview of your Knowledge Graph and pipeline jobs.
        </p>
      </div>

      <div className="grid grid-cols-4 gap-4">
        <StatCard
          title="Total Nodes"
          value={graphStats?.total_nodes?.toLocaleString() ?? "-"}
          icon={Network}
          description="All Neo4j nodes"
          loading={statsLoading}
        />
        <StatCard
          title="Relationships"
          value={graphStats?.total_relationships?.toLocaleString() ?? "-"}
          icon={ArrowLeftRight}
          description="All Neo4j edges"
          loading={statsLoading}
        />
        <StatCard
          title="Active Jobs"
          value={
            jobs
              ? jobs.filter((j) => j.status === "running" || j.status === "queued").length
              : "-"
          }
          icon={Loader2}
          description="Running + queued"
          loading={jobsLoading}
        />
        <StatCard
          title="System Status"
          value={
            systemOk ? (
              <span className="flex items-center gap-1.5 text-emerald-400">
                <CheckCircle2 className="size-5" /> Online
              </span>
            ) : (
              <span className="flex items-center gap-1.5 text-red-400">
                <XCircle className="size-5" /> Offline
              </span>
            )
          }
          icon={systemOk ? CheckCircle2 : XCircle}
          description={systemOk ? "API and Neo4j connected" : "Connection issue"}
          loading={!health}
        />
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Recent Jobs</CardTitle>
            <CardDescription>Build and pipeline jobs</CardDescription>
          </CardHeader>
          <CardContent className="p-0">
            <RecentJobsTable jobs={jobs ?? []} loading={jobsLoading} />
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-base">Knowledge Graph Stats</CardTitle>
            <CardDescription>Node and edge breakdown</CardDescription>
          </CardHeader>
          <CardContent>
            <GraphStatsGrid
              stats={
                graphStats
                  ? {
                      business_concepts: graphStats.business_concepts,
                      physical_tables: graphStats.physical_tables,
                      parent_chunks: graphStats.parent_chunks,
                      child_chunks: graphStats.child_chunks,
                      mentions_edges: graphStats.mentions_edges,
                      maps_to_edges: graphStats.maps_to_edges,
                    }
                  : null
              }
              loading={statsLoading}
            />
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Quick Actions</CardTitle>
        </CardHeader>
        <CardContent className="flex gap-3">
          <Button asChild>
            <Link to="/build">
              <Hammer className="mr-1.5 size-4" />
              Build Knowledge Graph
            </Link>
          </Button>
          <Button asChild variant="outline">
            <Link to="/query">
              <MessageSquare className="mr-1.5 size-4" />
              Query KG
            </Link>
          </Button>
          <Button asChild variant="secondary">
            <Link to="/ablation">
              <FlaskConical className="mr-1.5 size-4" />
              Run Ablation
            </Link>
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}
