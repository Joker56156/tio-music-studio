import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { api } from "../lib/api";
import type { GenerationRequest } from "../types/api";

export function useGenerateMusic() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (request: GenerationRequest) => api.generate(request),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["tracks"] });
    },
  });
}

export function useTaskStatus(taskId: string | null) {
  return useQuery({
    queryKey: ["task", taskId],
    queryFn: () => api.getTaskStatus(taskId!),
    enabled: !!taskId,
    refetchInterval: (query) => {
      const status = query.state.data?.status;
      if (status === "SUCCESS" || status === "FAILURE") return false;
      if ((query.state.data?.progress ?? 0) > 80) return 1000;
      return 2000;
    },
  });
}

export function useTracks() {
  return useQuery({
    queryKey: ["tracks"],
    queryFn: () => api.listTracks(),
  });
}

export function useGpuStatus() {
  return useQuery({
    queryKey: ["gpu-status"],
    queryFn: () => api.gpuStatus(),
    refetchInterval: 30000,
  });
}
