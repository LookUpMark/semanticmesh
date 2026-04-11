import { useState, useRef, useEffect } from "react";
import {
  Send,
  Loader2,
  ChevronDown,
  ChevronRight,
  Sparkles,
  ShieldCheck,
  ShieldAlert,
  MessageSquare,
  Trash2,
  BookOpen,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Progress } from "@/components/ui/progress";
import { useAppState, type ChatMessage } from "@/contexts/AppStateContext";
import { useSettings } from "@/contexts/SettingsContext";
import { useActiveKGSnapshot } from "@/hooks/useKGSnapshots";
import { useSubmitQuery } from "@/hooks/useJobs";
import { KGSnapshotManager } from "@/components/KGSnapshotManager";
import { ConversationSidebar } from "@/components/ConversationSidebar";
import type { QueryResponse, ConversationMessage } from "@/types/api";

// ── Utility functions ─────────────────────────────────────────────────────

function renderMarkdown(text: string): React.ReactNode {
  return text.split("\n").map((line, i, arr) => {
    const parts = line.split(/(\*\*[^*]+\*\*)/g).map((part, j) =>
      part.startsWith("**") && part.endsWith("**")
        ? <strong key={j}>{part.slice(2, -2)}</strong>
        : part
    );
    const isBullet = line.startsWith("- ") || line.startsWith("• ");
    if (isBullet) {
      return (
        <span key={i} className="block pl-4 before:content-['•'] before:mr-2 before:text-muted-foreground">
          {parts.map((p, j) => typeof p === "string" ? (isBullet && j === 0 ? p.replace(/^[•-]\s/, "") : p) : p)}
        </span>
      );
    }
    return (
      <span key={i}>
        {parts}{i < arr.length - 1 && "\n"}
      </span>
    );
  });
}

const EXAMPLE_QUESTIONS = [
  "What information is stored for each customer?",
  "How are products and orders related?",
  "What fields does the orders table contain?",
  "Describe the relationship between customers and payments.",
  "What business concepts are tracked in the knowledge graph?",
];

function AnswerMetadata({ data }: { data: QueryResponse }) {
  const [expanded, setExpanded] = useState(false);

  return (
    <div className="mt-2">
      <button
        onClick={() => setExpanded(!expanded)}
        className="flex items-center gap-1 text-xs text-muted-foreground hover:text-foreground transition-colors"
      >
        {expanded ? (
          <ChevronDown className="size-3" />
        ) : (
          <ChevronRight className="size-3" />
        )}
        Answer Metadata
      </button>

      {expanded && (
        <div className="mt-2 space-y-2 rounded-md border border-border bg-muted/30 p-3">
          <div className="grid grid-cols-2 gap-3">
            <div className="col-span-2">
              <p className="text-xs text-muted-foreground mb-1">Quality Score</p>
              <div className="flex items-center gap-2">
                <Progress
                  value={data.retrieval_quality_score * 100}
                  className="h-1.5 flex-1"
                />
                <span className="text-xs font-medium tabular-nums w-10 text-right">
                  {(data.retrieval_quality_score * 100).toFixed(1)}%
                </span>
              </div>
            </div>
            <div>
              <p className="text-xs text-muted-foreground">Chunks Retrieved</p>
              <p className="text-sm font-medium">{data.retrieval_chunk_count}</p>
            </div>
            <div>
              <p className="text-xs text-muted-foreground">Gate Decision</p>
              <Badge
                variant={
                  data.gate_decision === "proceed" ? "default" : "destructive"
                }
              >
                {data.gate_decision}
              </Badge>
            </div>
            <div>
              <p className="text-xs text-muted-foreground">Grounded</p>
              {data.grounded ? (
                <Badge variant="default" className="gap-1 bg-emerald-600">
                  <ShieldCheck className="size-3" /> Grounded
                </Badge>
              ) : (
                <Badge variant="destructive" className="gap-1">
                  <ShieldAlert className="size-3" /> Not Grounded
                </Badge>
              )}
            </div>
          </div>

          {data.sources.length > 0 && (
            <div>
              <p className="text-xs text-muted-foreground mb-1">Sources</p>
              <div className="flex flex-wrap gap-1">
                {data.sources.map((s, i) => (
                  <Badge key={i} variant="outline" className="text-xs font-mono">
                    {s.length > 40 ? s.slice(0, 40) + "..." : s}
                  </Badge>
                ))}
              </div>
            </div>
          )}

          {data.context_previews.length > 0 && (
            <div>
              <p className="text-xs text-muted-foreground mb-1">
                Context Previews
              </p>
              <div className="space-y-1">
                {data.context_previews.map((preview, i) => (
                  <div
                    key={i}
                    className="rounded border border-border bg-background p-2 text-xs text-muted-foreground"
                  >
                    {preview}...
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export function QueryPage() {
  const {
    queryMessages: messages,
    setQueryMessages: setMessages,
    sessionId,
    resetSession,
    loadConversation,
  } = useAppState();
  const { getGlobalPipelineConfig } = useSettings();
  const { data: activeSnapshot } = useActiveKGSnapshot();
  const [input, setInput] = useState("");
  const [showSidebar, setShowSidebar] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  const submitQuery = useSubmitQuery();
  const isLoading = submitQuery.isPending;

  // Auto-scroll on new messages
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSend = () => {
    const question = input.trim();
    if (!question || isLoading) return;

    const userMessage: ChatMessage = { role: "user", content: question };
    const loadingMessage: ChatMessage = { role: "assistant", content: "", isLoading: true };

    setMessages((prev) => [...prev, userMessage, loadingMessage]);
    setInput("");

    submitQuery.mutate(
      { question, config: getGlobalPipelineConfig(), session_id: sessionId },
      {
        onSuccess: (data) => {
          const assistantMessage: ChatMessage = {
            role: "assistant",
            content: data.answer,
            metadata: data,
          };
          setMessages((prev) => [...prev.slice(0, -1), assistantMessage]);
        },
        onError: () => {
          setMessages((prev) => [
            ...prev.slice(0, -1),
            { role: "assistant", content: "An error occurred. Please try again." },
          ]);
        },
      }
    );
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleExampleClick = (question: string) => {
    setInput(question);
    inputRef.current?.focus();
  };

  const handleConversationLoad = ({
    sessionId: savedSessionId,
    messages: savedMessages,
  }: {
    sessionId: string;
    messages: Array<{ role: string; content: string; metadata?: QueryResponse | null }>;
  }) => {
    const chatMessages: ChatMessage[] = savedMessages.map((m) => ({
      role: m.role as "user" | "assistant",
      content: m.content,
      metadata: m.metadata ?? undefined,
    }));
    loadConversation(savedSessionId, chatMessages);
    setShowSidebar(false);
  };

  const hasMessages = messages.length > 0;

  return (
    <div className="flex h-full">
      {/* Conversation sidebar */}
      {showSidebar && (
        <ConversationSidebar
          sessionId={sessionId}
          currentMessages={messages as ConversationMessage[]}
          activeSnapshotId={activeSnapshot?.id ?? null}
          onLoad={handleConversationLoad}
          onNew={() => {
            resetSession();
            setShowSidebar(false);
          }}
        />
      )}

      {/* Main chat area */}
      <div className="flex h-full flex-col flex-1 min-w-0">
        {/* Header */}
        <div className="border-b border-border px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Button
                variant={showSidebar ? "secondary" : "ghost"}
                size="sm"
                className="gap-1.5"
                onClick={() => setShowSidebar((v) => !v)}
                title="Toggle conversation history"
              >
                <BookOpen className="size-4" />
                <span className="hidden sm:inline text-xs">History</span>
              </Button>
              <div>
                <h1 className="text-2xl font-bold tracking-tight">
                  Query Knowledge Graph
                </h1>
                <p className="text-sm text-muted-foreground">
                  Ask questions about your data using natural language.
                </p>
              </div>
            </div>
            {messages.length > 0 && (
              <Button
                variant="ghost"
                size="sm"
                onClick={resetSession}
                className="gap-2 text-muted-foreground"
              >
                <Trash2 className="size-4" />
                Clear
              </Button>
            )}
          </div>
        </div>

        {/* KG Selector */}
        <KGSnapshotManager variant="bar" />

        {/* Chat area */}
        <ScrollArea className="flex-1 px-6" ref={scrollRef}>
          {!hasMessages ? (
            <div className="flex flex-col items-center justify-center py-20">
              <div className="mb-6 flex size-16 items-center justify-center rounded-full bg-primary/10">
                <Sparkles className="size-8 text-primary" />
              </div>
              <h2 className="mb-2 text-lg font-semibold">
                Ask a question about your Knowledge Graph
              </h2>
              <p className="mb-6 text-sm text-muted-foreground">
                Try one of these example questions:
              </p>
              <div className="flex flex-wrap justify-center gap-2 max-w-xl">
                {EXAMPLE_QUESTIONS.map((q) => (
                  <button
                    key={q}
                    onClick={() => handleExampleClick(q)}
                    className="rounded-full border border-border bg-card px-3 py-1.5 text-xs text-muted-foreground transition-colors hover:bg-muted hover:text-foreground"
                  >
                    {q}
                  </button>
                ))}
              </div>
            </div>
          ) : (
            <div className="space-y-4 py-4">
              {messages.map((msg, idx) => (
                <div
                  key={idx}
                  className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
                >
                  <div
                    className={`max-w-[80%] rounded-lg px-4 py-3 ${
                      msg.role === "user"
                        ? "bg-primary text-primary-foreground"
                        : "bg-card border border-border"
                    }`}
                  >
                    {msg.isLoading ? (
                      <div className="flex items-center gap-2 text-muted-foreground">
                        <Loader2 className="size-4 animate-spin" />
                        <span className="text-sm">Searching the Knowledge Graph...</span>
                      </div>
                    ) : (
                      <>
                        <div className="flex items-start gap-2">
                          {msg.role === "assistant" && (
                            <MessageSquare className="mt-0.5 size-4 shrink-0 text-muted-foreground" />
                          )}
                          <div className="text-sm whitespace-pre-wrap leading-relaxed">
                            {renderMarkdown(msg.content)}
                          </div>
                        </div>
                        {msg.metadata && <AnswerMetadata data={msg.metadata} />}
                      </>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </ScrollArea>

        {/* Input bar */}
        <div className="border-t border-border p-4">
          <div className="mx-auto flex max-w-3xl items-end gap-3">
            <Textarea
              ref={inputRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask a question about your Knowledge Graph..."
              className="min-h-[44px] max-h-[120px] resize-none"
              rows={1}
              disabled={isLoading}
            />
            <Button onClick={handleSend} disabled={!input.trim() || isLoading} size="lg">
              {isLoading ? (
                <Loader2 className="size-4 animate-spin" />
              ) : (
                <Send className="size-4" />
              )}
            </Button>
          </div>
          <p className="mt-2 text-center text-xs text-muted-foreground">
            Press Enter to send, Shift+Enter for a new line
          </p>
        </div>
      </div>
    </div>
  );
}
