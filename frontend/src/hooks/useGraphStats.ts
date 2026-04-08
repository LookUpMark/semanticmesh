import { useQuery } from "@tanstack/react-query";
import { getGraphStats } from "@/lib/api";

export function useGraphStats() {
  return useQuery({
    queryKey: ["graphStats"],
    queryFn: getGraphStats,
    refetchInterval: 30_000,
    staleTime: 10_000,
    retry: 2,
  });
}
