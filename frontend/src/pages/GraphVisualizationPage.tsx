import { useEffect, useRef, useState, useCallback } from "react";
import {
  ZoomIn,
  ZoomOut,
  Maximize,
  Play,
  Pause,
  Filter,
  X,
  Network,
  Info,
  Upload,
  ChevronRight,
  Hash,
  FolderOpen,
  ArrowRight,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import { Separator } from "@/components/ui/separator";
import { ScrollArea } from "@/components/ui/scroll-area";
import { useGraphStats } from "@/hooks/useGraphStats";
import { getGraphData } from "@/lib/api";

// ── Theme Colors ──────────────────────────────────────────────────────────────
const THEME = {
  red: "#e94560",       // BusinessConcept
  blue: "#0f3460",      // PhysicalTable
  green: "#1a7a4a",     // ParentChunk
  teal: "#0d6e6e",      // Chunk
  gray: "#a8a8b3",      // Edges
  bg: "#0f0f23",        // Canvas background
  surface: "#16213e",   // Panel background
  highlight: "#e94560", // Active selection
} as const;

const NODE_COLORS: Record<string, string> = {
  BusinessConcept: THEME.red,
  PhysicalTable: THEME.blue,
  ParentChunk: THEME.green,
  Chunk: THEME.teal,
  default: THEME.gray,
};

const NODE_LABELS: Record<string, string> = {
  BusinessConcept: "Business Concept",
  PhysicalTable: "Physical Table",
  ParentChunk: "Parent Chunk",
  Chunk: "Chunk",
};

const EDGE_COLORS: Record<string, string> = {
  MAPPED_TO: THEME.red,
  MAPS_TO: THEME.red,
  REFERENCES: THEME.blue,
  MENTIONS: THEME.gray,
  CHILD_OF: THEME.green,
  default: THEME.gray,
};

// ── Types ─────────────────────────────────────────────────────────────────────
interface NodeData {
  id: string;
  label: string;
  group: string;
  confidence?: number;
  properties?: Record<string, unknown>;
}

interface EdgeData {
  id: string;
  from: string;
  to: string;
  label: string;
  confidence?: number;
}

interface VisNode {
  id: string;
  label: string;
  group: string;
  color: {
    background: string;
    border: string;
    highlight: { background: string; border: string };
  };
  font: { color: string; size: number };
  borderWidth: number;
  shadow: boolean;
}

interface VisEdge {
  id: string;
  from: string;
  to: string;
  label: string;
  font: { color: string; size: number; strokeWidth: number; background?: string };
  color: { color: string; highlight: string; opacity?: number };
  arrows: string;
  smooth: { type: string };
  width: number;
}

interface ImportedGraph {
  nodes?: NodeData[];
  edges?: EdgeData[];
}

// ── Physics ───────────────────────────────────────────────────────────────────
const PHYSICS_OPTIONS = {
  enabled: true,
  solver: "forceAtlas2Based",
  forceAtlas2Based: {
    gravitationalConstant: -80,
    centralGravity: 0.01,
    springLength: 130,
    springConstant: 0.08,
  },
  stabilization: {
    iterations: 150,
  },
};

// ── Helpers ───────────────────────────────────────────────────────────────────
function nodeColor(group: string) {
  const c = NODE_COLORS[group] || NODE_COLORS.default;
  return {
    background: c,
    border: c,
    highlight: { background: c, border: "#ffffff" },
  };
}

function edgeColor(label: string) {
  const c = EDGE_COLORS[label] || EDGE_COLORS.default;
  return { color: c, highlight: "#ffffff", opacity: 0.7 };
}

function toVisNode(n: NodeData): VisNode {
  const c = nodeColor(n.group);
  return {
    id: n.id,
    label: n.label,
    group: n.group,
    color: c,
    font: { color: "#e2e8f0", size: 12 },
    borderWidth: 2,
    shadow: true,
  };
}

function toVisEdge(e: EdgeData): VisEdge {
  const c = edgeColor(e.label);
  return {
    id: e.id,
    from: e.from,
    to: e.to,
    label: e.label,
    font: { color: THEME.gray, size: 10, strokeWidth: 0 },
    color: c,
    arrows: "to",
    smooth: { type: "continuous" },
    width: 1.5,
  };
}

// ── Component ─────────────────────────────────────────────────────────────────
export function GraphVisualizationPage() {
  const containerRef = useRef<HTMLDivElement>(null);
  const networkRef = useRef<unknown>(null);
  const visNodesRef = useRef<unknown>(null);
  const visEdgesRef = useRef<unknown>(null);

  const [physicsEnabled, setPhysicsEnabled] = useState(true);
  const [selectedNode, setSelectedNode] = useState<NodeData | null>(null);
  const [detailsOpen, setDetailsOpen] = useState(false);

  // Filters
  const [nodeTypeFilters, setNodeTypeFilters] = useState<Record<string, boolean>>({
    BusinessConcept: true,
    PhysicalTable: true,
    ParentChunk: true,
    Chunk: true,
  });
  const [edgeTypeFilters, setEdgeTypeFilters] = useState<Record<string, boolean>>({
    MAPPED_TO: true,
    MAPS_TO: true,
    REFERENCES: true,
    MENTIONS: true,
    CHILD_OF: true,
  });

  // Counts
  const [nodeCount, setNodeCount] = useState(0);
  const [edgeCount, setEdgeCount] = useState(0);
  const [loading, setLoading] = useState(true);

  // Incremental animation progress
  const [animationProgress, setAnimationProgress] = useState<{
    phase: "nodes" | "edges";
    current: number;
    total: number;
  } | null>(null);
  const animationTimerRef = useRef<ReturnType<typeof setInterval> | null>(null);

  // Drag-and-drop state
  const [dragOver, setDragOver] = useState(false);

  // Remote stats
  const { data: stats } = useGraphStats();

  // All loaded raw data (before filtering)
  const [allNodes, setAllNodes] = useState<NodeData[]>([]);
  const [allEdges, setAllEdges] = useState<EdgeData[]>([]);

  // ── Sample data ─────────────────────────────────────────────────────────────
  const generateSampleData = useCallback((): { nodes: NodeData[]; edges: EdgeData[] } => {
    const conceptNames = [
      "Customer", "Product", "Order", "Payment", "Category",
      "Inventory", "Shipping", "Invoice", "Review", "Wishlist",
    ];
    const tableNames = [
      "customers", "products", "orders", "payments", "categories",
      "inventory", "shipments", "invoices", "reviews",
    ];

    const nodes: NodeData[] = [];
    const edges: EdgeData[] = [];

    conceptNames.forEach((name, i) => {
      nodes.push({
        id: `bc-${i}`,
        label: name,
        group: "BusinessConcept",
        confidence: Math.round((0.75 + Math.random() * 0.25) * 100),
        properties: { description: `${name} business concept`, source: "glossary" },
      });
    });

    tableNames.forEach((name, i) => {
      nodes.push({
        id: `pt-${i}`,
        label: name,
        group: "PhysicalTable",
        confidence: Math.round((0.80 + Math.random() * 0.20) * 100),
        properties: {
          columns: ["id", "name", "created_at"],
          schema: "public",
        },
      });
    });

    // MAPS_TO edges: concept -> table
    for (let i = 0; i < Math.min(conceptNames.length, tableNames.length); i++) {
      edges.push({
        id: `e-map-${i}`,
        from: `bc-${i}`,
        to: `pt-${i}`,
        label: "MAPS_TO",
        confidence: Math.round((0.70 + Math.random() * 0.30) * 100),
      });
    }

    // MENTIONS edges: concept -> concept
    edges.push(
      { id: "e-men-0", from: "bc-0", to: "bc-2", label: "MENTIONS", confidence: 95 },
      { id: "e-men-1", from: "bc-1", to: "bc-2", label: "MENTIONS", confidence: 88 },
      { id: "e-men-2", from: "bc-0", to: "bc-3", label: "MENTIONS", confidence: 92 },
      { id: "e-men-3", from: "bc-2", to: "bc-5", label: "MENTIONS", confidence: 85 },
      { id: "e-men-4", from: "bc-6", to: "bc-2", label: "MENTIONS", confidence: 78 },
    );

    // REFERENCES edges: table -> table (FK)
    edges.push(
      { id: "e-ref-0", from: "pt-0", to: "pt-2", label: "REFERENCES", confidence: 99 },
      { id: "e-ref-1", from: "pt-1", to: "pt-2", label: "REFERENCES", confidence: 97 },
      { id: "e-ref-2", from: "pt-2", to: "pt-3", label: "REFERENCES", confidence: 96 },
    );

    return { nodes, edges };
  }, []);

  // ── Build / rebuild network ─────────────────────────────────────────────────
  const buildNetwork = useCallback(
    (nodes: NodeData[], edges: EdgeData[]) => {
      if (!containerRef.current) return;

      // Destroy old network if any
      if (networkRef.current) {
        (networkRef.current as { destroy: () => void }).destroy();
        networkRef.current = null;
      }

      // Filter
      const filteredNodes = nodes.filter((n) => nodeTypeFilters[n.group] !== false);
      const visibleNodeIds = new Set(filteredNodes.map((n) => n.id));
      const filteredEdges = edges.filter(
        (e) =>
          edgeTypeFilters[e.label] !== false &&
          visibleNodeIds.has(e.from) &&
          visibleNodeIds.has(e.to),
      );

      const _seenN = new Set<string>();
      const visNodesArr = filteredNodes.map(toVisNode).filter((n) => {
        if (_seenN.has(n.id)) return false;
        _seenN.add(n.id);
        return true;
      });
      const _seenE = new Set<string>();
      const visEdgesArr = filteredEdges.map(toVisEdge).filter((e) => {
        if (_seenE.has(e.id)) return false;
        _seenE.add(e.id);
        return true;
      });

      // Dynamic import then create
      Promise.all([import("vis-network"), import("vis-data")]).then(([vis, { DataSet }]) => {
        if (!containerRef.current) return;

        const visNodes = new DataSet(visNodesArr);
        const visEdges = new DataSet(visEdgesArr);

        visNodesRef.current = visNodes;
        visEdgesRef.current = visEdges;

        const options = {
          physics: { ...PHYSICS_OPTIONS, enabled: physicsEnabled },
          interaction: {
            hover: true,
            tooltipDelay: 200,
            zoomView: true,
            dragView: true,
          },
          nodes: {
            shape: "dot" as const,
            size: 16,
          },
          edges: {
            width: 1.5,
          },
          groups: {
            BusinessConcept: {
              color: {
                background: THEME.red,
                border: THEME.red,
              },
            },
            PhysicalTable: {
              color: {
                background: THEME.blue,
                border: THEME.blue,
              },
            },
            ParentChunk: {
              color: {
                background: THEME.green,
                border: THEME.green,
              },
              shape: "square" as const,
              size: 10,
            },
            Chunk: {
              color: {
                background: THEME.teal,
                border: THEME.teal,
              },
              shape: "triangle" as const,
              size: 8,
            },
          },
        };

        const network = new vis.Network(
          containerRef.current,
          { nodes: visNodes, edges: visEdges },
          options,
        );

        network.on("click", (params: { nodes: string[] }) => {
          if (params.nodes.length > 0) {
            const nodeId = params.nodes[0];
            const nodeData = visNodes.get(nodeId);
            const original = nodes.find((n) => n.id === nodeId);
            setSelectedNode({
              id: nodeId,
              label: nodeData.label as string,
              group: nodeData.group as string,
              confidence: original?.confidence,
              properties: original?.properties,
            });
            setDetailsOpen(true);
          } else {
            setSelectedNode(null);
            setDetailsOpen(false);
          }
        });

        networkRef.current = network;
        setNodeCount(visNodes.length);
        setEdgeCount(visEdges.length);
        setLoading(false);
      });
    },
    [nodeTypeFilters, edgeTypeFilters, physicsEnabled],
  );

  // ── Build network with incremental animation ────────────────────────────────
  const buildNetworkIncremental = useCallback(
    (nodes: NodeData[], edges: EdgeData[]) => {
      if (!containerRef.current) return;

      // Cancel any running animation
      if (animationTimerRef.current) {
        clearInterval(animationTimerRef.current);
        animationTimerRef.current = null;
      }

      // Destroy old network if any
      if (networkRef.current) {
        (networkRef.current as { destroy: () => void }).destroy();
        networkRef.current = null;
      }

      // Filter
      const filteredNodes = nodes.filter((n) => nodeTypeFilters[n.group] !== false);
      const visibleNodeIds = new Set(filteredNodes.map((n) => n.id));
      const filteredEdges = edges.filter(
        (e) =>
          edgeTypeFilters[e.label] !== false &&
          visibleNodeIds.has(e.from) &&
          visibleNodeIds.has(e.to),
      );

      // Deduplicate by id before batching — DataSet.add() throws on duplicate ids
      // within the same array, even across separate batch calls on the same DataSet.
      const seenNodeIds = new Set<string>();
      const visNodesArr = filteredNodes
        .map(toVisNode)
        .filter((n) => {
          if (seenNodeIds.has(n.id)) return false;
          seenNodeIds.add(n.id);
          return true;
        });

      const seenEdgeIds = new Set<string>();
      const visEdgesArr = filteredEdges
        .map(toVisEdge)
        .filter((e) => {
          if (seenEdgeIds.has(e.id)) return false;
          seenEdgeIds.add(e.id);
          return true;
        });

      Promise.all([import("vis-network"), import("vis-data")]).then(
        ([vis, { DataSet }]) => {
          if (!containerRef.current) return;

          // Start with empty datasets — we'll fill them incrementally
          const visNodes = new DataSet<VisNode>([]);
          const visEdges = new DataSet<VisEdge>([]);

          visNodesRef.current = visNodes;
          visEdgesRef.current = visEdges;

          const options = {
            physics: { ...PHYSICS_OPTIONS, enabled: physicsEnabled },
            interaction: {
              hover: true,
              tooltipDelay: 200,
              zoomView: true,
              dragView: true,
            },
            nodes: { shape: "dot" as const, size: 16 },
            edges: { width: 1.5 },
            groups: {
              BusinessConcept: { color: { background: THEME.red, border: THEME.red } },
              PhysicalTable: { color: { background: THEME.blue, border: THEME.blue } },
              ParentChunk: {
                color: { background: THEME.green, border: THEME.green },
                shape: "square" as const,
                size: 10,
              },
              Chunk: {
                color: { background: THEME.teal, border: THEME.teal },
                shape: "triangle" as const,
                size: 8,
              },
            },
          };

          const network = new vis.Network(
            containerRef.current,
            { nodes: visNodes, edges: visEdges },
            options,
          );

          network.on("click", (params: { nodes: string[] }) => {
            if (params.nodes.length > 0) {
              const nodeId = params.nodes[0];
              const nodeData = visNodes.get(nodeId);
              const original = nodes.find((n) => n.id === nodeId);
              setSelectedNode({
                id: nodeId,
                label: nodeData.label as string,
                group: nodeData.group as string,
                confidence: original?.confidence,
                properties: original?.properties,
              });
              setDetailsOpen(true);
            } else {
              setSelectedNode(null);
              setDetailsOpen(false);
            }
          });

          networkRef.current = network;
          setLoading(false);

          if (visNodesArr.length === 0) {
            setNodeCount(0);
            setEdgeCount(0);
            return;
          }

          // ~50 ticks total regardless of graph size
          const NODE_BATCH = Math.max(1, Math.ceil(visNodesArr.length / 50));
          let nodeIdx = 0;

          setAnimationProgress({ phase: "nodes", current: 0, total: visNodesArr.length });

          animationTimerRef.current = setInterval(() => {
            const batch = visNodesArr.slice(nodeIdx, nodeIdx + NODE_BATCH);
            // Use update() (upsert) instead of add() so SSE-pre-added nodes
            // don't cause "duplicate id" crashes.
            (visNodesRef.current as { update: (items: VisNode[]) => void }).update(batch);
            nodeIdx += batch.length;
            setNodeCount(nodeIdx);
            setAnimationProgress({ phase: "nodes", current: nodeIdx, total: visNodesArr.length });

            if (nodeIdx >= visNodesArr.length) {
              clearInterval(animationTimerRef.current!);
              animationTimerRef.current = null;

              // Start edge animation
              const EDGE_BATCH = Math.max(1, Math.ceil(visEdgesArr.length / 40));
              let edgeIdx = 0;

              if (visEdgesArr.length === 0) {
                setEdgeCount(0);
                setAnimationProgress(null);
                return;
              }

              setAnimationProgress({ phase: "edges", current: 0, total: visEdgesArr.length });

              animationTimerRef.current = setInterval(() => {
                const eBatch = visEdgesArr.slice(edgeIdx, edgeIdx + EDGE_BATCH);
                (visEdgesRef.current as { update: (items: VisEdge[]) => void }).update(eBatch);
                edgeIdx += eBatch.length;
                setEdgeCount(edgeIdx);
                setAnimationProgress({
                  phase: "edges",
                  current: edgeIdx,
                  total: visEdgesArr.length,
                });

                if (edgeIdx >= visEdgesArr.length) {
                  clearInterval(animationTimerRef.current!);
                  animationTimerRef.current = null;
                  setAnimationProgress(null);
                }
              }, 40);
            }
          }, 60);
        },
      );
    },
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [nodeTypeFilters, edgeTypeFilters, physicsEnabled],
  );

  // ── Init: load real graph data from backend ─────────────────────────────────
  useEffect(() => {
    let cancelled = false;
    setLoading(true);

    getGraphData()
      .then(({ nodes, edges }) => {
        if (cancelled) return;
        setAllNodes(nodes);
        setAllEdges(edges);
        if (nodes.length > 0) {
          buildNetworkIncremental(nodes, edges);
        } else {
          setLoading(false);
        }
      })
      .catch(() => {
        if (cancelled) return;
        // Backend unavailable — fall back to empty state
        setAllNodes([]);
        setAllEdges([]);
        setLoading(false);
      });

    return () => {
      cancelled = true;
      if (animationTimerRef.current) {
        clearInterval(animationTimerRef.current);
        animationTimerRef.current = null;
      }
      if (networkRef.current) {
        (networkRef.current as { destroy: () => void }).destroy();
      }
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // ── Rebuild on filter changes ───────────────────────────────────────────────
  useEffect(() => {
    if (allNodes.length > 0) {
      buildNetwork(allNodes, allEdges);
    } else {
      // Graph is empty — destroy any leftover network
      if (networkRef.current) {
        (networkRef.current as { destroy: () => void }).destroy();
        networkRef.current = null;
      }
      setNodeCount(0);
      setEdgeCount(0);
    }
  }, [nodeTypeFilters, edgeTypeFilters, physicsEnabled, allNodes, allEdges, buildNetwork]);

  // ── Toolbar handlers ────────────────────────────────────────────────────────
  const getNetwork = () =>
    networkRef.current as {
      fit: () => void;
      getScale: () => number;
      moveTo: (o: { scale: number }) => void;
      setOptions: (o: Record<string, unknown>) => void;
    } | null;

  const handleZoomIn = () => {
    const net = getNetwork();
    if (net) net.moveTo({ scale: net.getScale() * 1.3 });
  };

  const handleZoomOut = () => {
    const net = getNetwork();
    if (net) net.moveTo({ scale: net.getScale() / 1.3 });
  };

  const handleFit = () => {
    const net = getNetwork();
    if (net) net.fit();
  };

  const togglePhysics = () => {
    const next = !physicsEnabled;
    setPhysicsEnabled(next);
    const net = getNetwork();
    if (net) {
      net.setOptions({ physics: { ...PHYSICS_OPTIONS, enabled: next } });
    }
  };

  // ── Filter toggles ──────────────────────────────────────────────────────────
  const toggleNodeType = (type: string) =>
    setNodeTypeFilters((prev) => ({ ...prev, [type]: !prev[type] }));

  const toggleEdgeType = (type: string) =>
    setEdgeTypeFilters((prev) => ({ ...prev, [type]: !prev[type] }));

  // ── Drag-and-drop file upload ───────────────────────────────────────────────
  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragOver(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragOver(false);
  }, []);

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      e.stopPropagation();
      setDragOver(false);

      const files = Array.from(e.dataTransfer.files);
      if (files.length === 0) return;

      const file = files[0];
      const reader = new FileReader();
      reader.onload = (ev) => {
        try {
          const text = ev.target?.result as string;
          const data: ImportedGraph = JSON.parse(text);

          if (!data.nodes || !Array.isArray(data.nodes)) {
            console.error("Invalid format: expected { nodes: [...], edges: [...] }");
            return;
          }

          const importedNodes: NodeData[] = data.nodes.map((n, i) => ({
            id: String(n.id ?? `imported-${i}`),
            label: n.label ?? `Node ${i}`,
            group: n.group ?? "default",
            confidence: n.confidence,
            properties: n.properties,
          }));

          const importedEdges: EdgeData[] = (data.edges ?? []).map((e, i) => ({
            id: String(e.id ?? `imported-e-${i}`),
            from: String(e.from),
            to: String(e.to),
            label: e.label ?? "RELATED",
            confidence: e.confidence,
          }));

          setAllNodes(importedNodes);
          setAllEdges(importedEdges);
          setSelectedNode(null);
          setDetailsOpen(false);
          buildNetworkIncremental(importedNodes, importedEdges);
        } catch (err) {
          console.error("Failed to parse dropped file:", err);
        }
      };
      reader.readAsText(file);
    },
    [buildNetworkIncremental],
  );

  // ── Count unique types for stats ────────────────────────────────────────────
  const nodeTypeCounts = allNodes.reduce<Record<string, number>>((acc, n) => {
    acc[n.group] = (acc[n.group] || 0) + 1;
    return acc;
  }, {});

  const edgeTypeCounts = allEdges.reduce<Record<string, number>>((acc, e) => {
    acc[e.label] = (acc[e.label] || 0) + 1;
    return acc;
  }, {});

  // ── Connected edges for selected node ────────────────────────────────────────
  const connectedEdges = selectedNode
    ? allEdges.filter((e) => e.from === selectedNode.id || e.to === selectedNode.id)
    : [];

  const connectedNodes = selectedNode
    ? allNodes.filter(
        (n) =>
          connectedEdges.some((e) => e.from === n.id || e.to === n.id) &&
          n.id !== selectedNode.id,
      )
    : [];

  // ── Render ───────────────────────────────────────────────────────────────────
  return (
    <div className="flex h-full flex-col" style={{ height: "100%" }}>
      {/* ── Header / Toolbar ────────────────────────────────────────────────── */}
      <div className="flex items-center justify-between border-b border-border px-4 py-2">
        <div className="flex items-center gap-2">
          <Network className="size-5" style={{ color: THEME.red }} />
          <div>
            <h1 className="text-base font-semibold tracking-tight">
              Graph Visualization
            </h1>
            <p className="text-[11px] text-muted-foreground">
              Drag & drop a JSON file or explore the sample graph
            </p>
          </div>
        </div>

        <div className="flex items-center gap-1.5">
          <Button variant="outline" size="xs" onClick={handleZoomIn}>
            <ZoomIn className="size-3.5" />
          </Button>
          <Button variant="outline" size="xs" onClick={handleZoomOut}>
            <ZoomOut className="size-3.5" />
          </Button>
          <Button variant="outline" size="xs" onClick={handleFit}>
            <Maximize className="size-3.5" />
          </Button>
          <Separator orientation="vertical" className="mx-1 h-5" />
          <Button
            variant={physicsEnabled ? "default" : "outline"}
            size="xs"
            onClick={togglePhysics}
          >
            {physicsEnabled ? (
              <Pause className="size-3.5" />
            ) : (
              <Play className="size-3.5" />
            )}
            <span className="ml-1">Physics</span>
          </Button>
        </div>
      </div>

      {/* ── Main area ────────────────────────────────────────────────────────── */}
      <div className="flex flex-1 overflow-hidden">
        {/* ── Filters sidebar ──────────────────────────────────────────────── */}
        <div className="w-48 shrink-0 border-r border-border overflow-y-auto bg-card/50">
          <div className="p-3">
            <h3 className="mb-2 flex items-center gap-1.5 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
              <Filter className="size-3.5" /> Filters
            </h3>

            {/* Node type filters */}
            <p className="mb-1.5 text-[11px] font-medium text-muted-foreground">
              Node Types
            </p>
            <div className="space-y-1.5">
              {Object.entries(NODE_COLORS)
                .filter(([key]) => key !== "default")
                .map(([type, color]) => (
                  <div key={type} className="flex items-center gap-2">
                    <Switch
                      size="sm"
                      checked={nodeTypeFilters[type] !== false}
                      onCheckedChange={() => toggleNodeType(type)}
                    />
                    <Label className="flex items-center gap-1.5 text-xs cursor-pointer">
                      <span
                        className="inline-block size-2.5 rounded-full shrink-0"
                        style={{ backgroundColor: color }}
                      />
                      {NODE_LABELS[type] ?? type}
                    </Label>
                  </div>
                ))}
            </div>

            <Separator className="my-3" />

            {/* Edge type filters */}
            <p className="mb-1.5 text-[11px] font-medium text-muted-foreground">
              Edge Types
            </p>
            <div className="space-y-1.5">
              {Object.entries(EDGE_COLORS)
                .filter(([key]) => key !== "default")
                .map(([type, color]) => (
                  <div key={type} className="flex items-center gap-2">
                    <Switch
                      size="sm"
                      checked={edgeTypeFilters[type] !== false}
                      onCheckedChange={() => toggleEdgeType(type)}
                    />
                    <Label className="flex items-center gap-1.5 text-xs cursor-pointer">
                      <span
                        className="inline-block size-2.5 rounded-sm shrink-0"
                        style={{ backgroundColor: color }}
                      />
                      {type}
                    </Label>
                  </div>
                ))}
            </div>

            <Separator className="my-3" />

            {/* Import hint */}
            <div className="rounded-md border border-dashed border-border p-2 text-center">
              <Upload className="mx-auto mb-1 size-4 text-muted-foreground" />
              <p className="text-[10px] text-muted-foreground leading-tight">
                Drop a JSON file on the canvas to import a graph
              </p>
            </div>
          </div>
        </div>

        {/* ── Canvas ────────────────────────────────────────────────────────── */}
        <div className="relative flex-1">
          {loading && (
            <div className="absolute inset-0 z-10 flex items-center justify-center bg-background/80">
              <div className="flex items-center gap-2 text-muted-foreground">
                <Network className="size-5 animate-pulse" />
                <span className="text-sm">Loading graph...</span>
              </div>
            </div>
          )}

          {/* Incremental animation progress HUD */}
          {animationProgress && (
            <div className="absolute bottom-4 left-1/2 z-10 -translate-x-1/2">
              <div
                className="flex min-w-[220px] flex-col gap-1.5 rounded-lg border border-border px-4 py-2.5 shadow-lg"
                style={{ backgroundColor: THEME.surface }}
              >
                <div className="flex items-center justify-between gap-4 text-xs">
                  <span className="flex items-center gap-1.5 text-muted-foreground">
                    <Network className="size-3.5 animate-pulse" style={{ color: THEME.red }} />
                    {animationProgress.phase === "nodes"
                      ? `Adding nodes… ${animationProgress.current}/${animationProgress.total}`
                      : `Adding edges… ${animationProgress.current}/${animationProgress.total}`}
                  </span>
                  <span className="font-mono text-[10px] tabular-nums" style={{ color: THEME.red }}>
                    {Math.round((animationProgress.current / animationProgress.total) * 100)}%
                  </span>
                </div>
                <div className="h-1 w-full overflow-hidden rounded-full bg-muted">
                  <div
                    className="h-full rounded-full transition-all duration-75"
                    style={{
                      width: `${Math.round((animationProgress.current / animationProgress.total) * 100)}%`,
                      backgroundColor: animationProgress.phase === "nodes" ? THEME.red : THEME.blue,
                    }}
                  />
                </div>
              </div>
            </div>
          )}

          {/* Drag-and-drop overlay */}
          {dragOver && (
            <div className="absolute inset-0 z-20 flex items-center justify-center bg-background/70 backdrop-blur-sm">
              <div className="flex flex-col items-center gap-2 rounded-lg border-2 border-dashed p-8"
                   style={{ borderColor: THEME.red }}>
                <Upload className="size-8" style={{ color: THEME.red }} />
                <p className="text-sm font-medium">Drop JSON file to load graph</p>
                <p className="text-xs text-muted-foreground">
                  vis.js DataSet format: {"{ nodes: [...], edges: [...] }"}
                </p>
              </div>
            </div>
          )}

          {/* Empty state */}
          {nodeCount === 0 && !loading && (
            <div className="absolute inset-0 z-10 flex items-center justify-center">
              <div className="flex flex-col items-center gap-3 text-muted-foreground">
                <FolderOpen className="size-12" style={{ color: THEME.gray }} />
                <p className="text-sm font-medium">Knowledge Graph is empty</p>
                <p className="text-xs text-center max-w-xs">
                  Build the KG first from the KG Builder page, or
                  <br />
                  drag and drop a JSON file to visualize a local graph.
                </p>
              </div>
            </div>
          )}

          <div
            ref={containerRef}
            className="h-full w-full"
            style={{ backgroundColor: THEME.bg }}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
          />
        </div>

        {/* ── Node details slide-in panel ───────────────────────────────────── */}
        <div
          className="shrink-0 overflow-hidden border-l border-border transition-all duration-300 ease-in-out"
          style={{
            width: detailsOpen ? 280 : 0,
            backgroundColor: THEME.surface,
          }}
        >
          <ScrollArea className="h-full">
            {selectedNode && (
              <div className="p-4">
                {/* Header */}
                <div className="mb-4 flex items-start justify-between">
                  <h3 className="flex items-center gap-1.5 text-sm font-semibold">
                    <Info className="size-4" style={{ color: THEME.red }} />
                    Node Details
                  </h3>
                  <button
                    onClick={() => {
                      setDetailsOpen(false);
                      setSelectedNode(null);
                    }}
                    className="rounded p-0.5 text-muted-foreground hover:text-foreground transition-colors"
                  >
                    <X className="size-4" />
                  </button>
                </div>

                {/* Node name - highlighted */}
                <div className="mb-3 rounded-md p-2" style={{ backgroundColor: "rgba(233,69,96,0.1)" }}>
                  <p className="text-xs text-muted-foreground mb-0.5">Name</p>
                  <p
                    className="text-sm font-bold"
                    style={{ color: THEME.red }}
                  >
                    {selectedNode.label}
                  </p>
                </div>

                {/* Type badge */}
                <div className="mb-3">
                  <p className="text-xs text-muted-foreground mb-1">Type</p>
                  <Badge
                    variant="outline"
                    style={{
                      borderColor: NODE_COLORS[selectedNode.group] || THEME.gray,
                      color: NODE_COLORS[selectedNode.group] || THEME.gray,
                    }}
                  >
                    {selectedNode.group === "BusinessConcept"
                      ? "Business Concept"
                      : "Physical Table"}
                  </Badge>
                </div>

                {/* Confidence */}
                {selectedNode.confidence != null && (
                  <div className="mb-3">
                    <p className="text-xs text-muted-foreground mb-1">Confidence</p>
                    <div className="flex items-center gap-2">
                      <div className="h-1.5 flex-1 rounded-full bg-muted overflow-hidden">
                        <div
                          className="h-full rounded-full transition-all"
                          style={{
                            width: `${selectedNode.confidence}%`,
                            backgroundColor:
                              selectedNode.confidence >= 90
                                ? "#22c55e"
                                : selectedNode.confidence >= 70
                                  ? "#eab308"
                                  : THEME.red,
                          }}
                        />
                      </div>
                      <span className="text-xs font-mono font-medium">
                        {selectedNode.confidence}%
                      </span>
                    </div>
                  </div>
                )}

                {/* ID */}
                <div className="mb-3">
                  <p className="text-xs text-muted-foreground mb-0.5">ID</p>
                  <p className="font-mono text-xs bg-muted/50 rounded px-1.5 py-0.5 inline-block">
                    {selectedNode.id}
                  </p>
                </div>

                {/* Properties */}
                {selectedNode.properties &&
                  Object.keys(selectedNode.properties).length > 0 && (
                    <div className="mb-3">
                      <p className="text-xs text-muted-foreground mb-1.5">
                        Properties
                      </p>
                      <div className="space-y-1">
                        {Object.entries(selectedNode.properties).map(
                          ([key, value]) => (
                            <div
                              key={key}
                              className="rounded border border-border bg-muted/30 p-1.5"
                            >
                              <p className="text-[10px] text-muted-foreground">
                                {key}
                              </p>
                              <p className="text-xs font-mono">
                                {typeof value === "object"
                                  ? JSON.stringify(value)
                                  : String(value)}
                              </p>
                            </div>
                          ),
                        )}
                      </div>
                    </div>
                  )}

                <Separator className="my-3" />

                {/* Connections */}
                <div className="mb-3">
                  <p className="text-xs text-muted-foreground mb-1.5 flex items-center gap-1">
                    <Hash className="size-3" /> Connections ({connectedEdges.length})
                  </p>
                  <div className="space-y-1.5">
                    {connectedEdges.map((edge) => {
                      const otherNodeId =
                        edge.from === selectedNode.id ? edge.to : edge.from;
                      const otherNode = allNodes.find((n) => n.id === otherNodeId);
                      const isOutgoing = edge.from === selectedNode.id;
                      return (
                        <div
                          key={edge.id}
                          className="flex items-center gap-1.5 rounded border border-border bg-muted/30 p-1.5 text-[11px]"
                        >
                          <ArrowRight
                            className={`size-3 shrink-0 ${
                              isOutgoing ? "" : "rotate-180"
                            }`}
                            style={{ color: EDGE_COLORS[edge.label] || THEME.gray }}
                          />
                          <span
                            className="inline-block size-2 rounded-full shrink-0"
                            style={{
                              backgroundColor:
                                NODE_COLORS[otherNode?.group || ""] || THEME.gray,
                            }}
                          />
                          <span className="truncate font-medium">
                            {otherNode?.label || otherNodeId}
                          </span>
                          <Badge
                            variant="ghost"
                            className="ml-auto text-[9px] px-1 py-0 h-4"
                            style={{ color: EDGE_COLORS[edge.label] || THEME.gray }}
                          >
                            {edge.label}
                          </Badge>
                        </div>
                      );
                    })}
                    {connectedEdges.length === 0 && (
                      <p className="text-[11px] text-muted-foreground">
                        No connections
                      </p>
                    )}
                  </div>
                </div>

                {/* Connected nodes list */}
                {connectedNodes.length > 0 && (
                  <>
                    <Separator className="my-3" />
                    <div>
                      <p className="text-xs text-muted-foreground mb-1.5">
                        Connected Nodes ({connectedNodes.length})
                      </p>
                      <div className="space-y-1">
                        {connectedNodes.map((node) => (
                          <button
                            key={node.id}
                            className="flex w-full items-center gap-1.5 rounded px-1.5 py-1 text-left text-xs hover:bg-muted/50 transition-colors"
                            onClick={() => {
                              setSelectedNode(node);
                              // Focus node in the network
                              const net = getNetwork();
                              if (net) {
                                (net as unknown as { focus: (id: string, opts: Record<string, unknown>) => void }).focus(node.id, {
                                  scale: 1.5,
                                  animation: { duration: 400, easingFunction: "easeInOutQuad" as const },
                                });
                              }
                            }}
                          >
                            <span
                              className="inline-block size-2 rounded-full shrink-0"
                              style={{
                                backgroundColor:
                                  NODE_COLORS[node.group] || THEME.gray,
                              }}
                            />
                            <span className="truncate">{node.label}</span>
                            <ChevronRight className="ml-auto size-3 text-muted-foreground" />
                          </button>
                        ))}
                      </div>
                    </div>
                  </>
                )}
              </div>
            )}
          </ScrollArea>
        </div>
      </div>

      {/* ── Stats bar ───────────────────────────────────────────────────────── */}
      <div className="flex items-center justify-between border-t border-border bg-card px-4 py-1.5">
        <div className="flex items-center gap-3 text-[11px] text-muted-foreground">
          <span className="flex items-center gap-1">
            <Network className="size-3" /> Nodes: <strong className="text-foreground">{nodeCount}</strong>
          </span>
          <span className="text-border">|</span>
          <span>
            Edges: <strong className="text-foreground">{edgeCount}</strong>
          </span>
          <span className="text-border">|</span>
          <span>
            Physics: <strong className="text-foreground">{physicsEnabled ? "On" : "Off"}</strong>
          </span>
        </div>

        <div className="flex items-center gap-3 text-[11px]">
          {/* Node type counts */}
          {Object.entries(nodeTypeCounts).map(([type, count]) => (
            <span key={type} className="flex items-center gap-1 text-muted-foreground">
              <span
                className="inline-block size-2 rounded-full"
                style={{ backgroundColor: NODE_COLORS[type] || THEME.gray }}
              />
              {type === "BusinessConcept" ? "Concepts" : "Tables"}:{" "}
              <strong className="text-foreground">{count}</strong>
            </span>
          ))}

          <span className="text-border">|</span>

          {/* Edge type counts */}
          {Object.entries(edgeTypeCounts).map(([type, count]) => (
            <span key={type} className="flex items-center gap-1 text-muted-foreground">
              <span
                className="inline-block size-2 rounded-sm"
                style={{ backgroundColor: EDGE_COLORS[type] || THEME.gray }}
              />
              {type}: <strong className="text-foreground">{count}</strong>
            </span>
          ))}

          {/* Remote stats */}
          {stats && (
            <>
              <span className="text-border">|</span>
              <span className="text-muted-foreground">
                Remote total: <strong className="text-foreground">{stats.total_nodes}</strong> nodes,{" "}
                <strong className="text-foreground">{stats.total_relationships}</strong> rels
              </span>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
