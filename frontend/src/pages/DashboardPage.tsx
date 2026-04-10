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
  Inbox,
  Trash2,
} from "lucide-react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button, buttonVariants } from "@/components/ui/button";
import { cn } from "@/lib/utils";
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
import { useDemoJobs, useHealth, useClearGraph } from "@/hooks/useJobs";
import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTrigger,
} from "@/components/ui/dialog";
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
  accentClass,
}: {
  title: string;
  value: React.ReactNode;
  icon: React.ElementType;
  description?: string;
  loading?: boolean;
  accentClass?: string;
}) {
  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between pb-2">
        <CardTitle className="text-sm font-medium text-muted-foreground">
          {title}
        </CardTitle>
        <Icon className={`size-4 ${accentClass ?? "text-muted-foreground"}`} />
      </CardHeader>
      <CardContent>
        {loading ? (
          <Skeleton className="h-8 w-20" />
        ) : (
          <>
            <div className={`text-2xl font-bold ${accentClass ?? ""}`}>{value}</div>
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
        <Inbox className="mb-2 size-8 text-muted-foreground/50" />
        <p className="text-sm font-medium text-muted-foreground">No jobs yet</p>
        <p className="text-xs text-muted-foreground/60">
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
              {job.job_id?.slice(0, 8) ?? "—"}...
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
    { key: "child_of_edges", label: "CHILD_OF Edges" },
    { key: "references_edges", label: "FK References" },
  ];

  return (
    <div className="grid grid-cols-4 gap-3">
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
  const clearGraph = useClearGraph();

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
          accentClass={(graphStats?.total_nodes ?? 0) > 0 ? "text-primary" : undefined}
        />
        <StatCard
          title="Relationships"
          value={graphStats?.total_relationships?.toLocaleString() ?? "-"}
          icon={ArrowLeftRight}
          description="All Neo4j edges"
          loading={statsLoading}
          accentClass={(graphStats?.total_relationships ?? 0) > 0 ? "text-primary" : undefined}
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
          accentClass={
            (jobs ?? []).filter((j) => j.status === "running" || j.status === "queued").length > 0
              ? "text-amber-400"
              : undefined
          }
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
        <CardContent className="flex flex-wrap gap-3">
          <Link to="/build" className={cn(buttonVariants({ variant: "default" }))}>
            <Hammer className="mr-1.5 size-4" />
            Build Knowledge Graph
          </Link>
          <Link to="/query" className={cn(buttonVariants({ variant: "outline" }))}>
            <MessageSquare className="mr-1.5 size-4" />
            Query KG
          </Link>
          <Link to="/ablation" className={cn(buttonVariants({ variant: "secondary" }))}>
            <FlaskConical className="mr-1.5 size-4" />
            Run Ablation
          </Link>

          <Dialog>
            <DialogTrigger asChild>
              <Button
                variant="destructive"
                disabled={clearGraph.isPending || (graphStats?.total_nodes ?? 0) === 0}
              >
                {clearGraph.isPending ? (
                  <Loader2 className="mr-1.5 size-4 animate-spin" />
                ) : (
                  <Trash2 className="mr-1.5 size-4" />
                )}
                Clear Graph
              </Button>
            </DialogTrigger>
            <DialogContent showCloseButton={false}>
              <DialogHeader>
                <p className="text-base font-semibold">Clear Knowledge Graph?</p>
                <p className="text-sm text-muted-foreground">
                  This will permanently delete{" "}
                  <strong>all {graphStats?.total_nodes?.toLocaleString()} nodes</strong> and{" "}
                  <strong>{graphStats?.total_relationships?.toLocaleString()} relationships</strong>{" "}
                  from Neo4j. This action cannot be undone.
                </p>
              </DialogHeader>
              <DialogFooter>
                <DialogClose asChild>
                  <Button variant="outline">Cancel</Button>
                </DialogClose>
                <DialogClose asChild>
                  <Button
                    variant="destructive"
                    onClick={() => clearGraph.mutate()}
                  >
                    Yes, clear graph
                  </Button>
                </DialogClose>
              </DialogFooter>
            </DialogContent>
          </Dialog>
        </CardContent>
      </Card>
    </div>
  );
}
