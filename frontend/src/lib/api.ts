import axios from "axios";
import type {
  GenerationRequest,
  GenerateResponse,
  TaskStatus,
  Track,
} from "../types/api";

const client = axios.create({
  baseURL: "/api",
  headers: { "Content-Type": "application/json" },
});

export const api = {
  // Generation
  generate: async (request: GenerationRequest): Promise<GenerateResponse> => {
    const { data } = await client.post<GenerateResponse>("/generate", request);
    return data;
  },

  getTaskStatus: async (taskId: string): Promise<TaskStatus> => {
    const { data } = await client.get<TaskStatus>(`/tasks/${taskId}`);
    return data;
  },

  // Tracks
  listTracks: async (params?: {
    limit?: number;
    offset?: number;
    favorites_only?: boolean;
  }): Promise<Track[]> => {
    const { data } = await client.get<Track[]>("/tracks", { params });
    return data;
  },

  getTrack: async (trackId: string): Promise<Track> => {
    const { data } = await client.get<Track>(`/tracks/${trackId}`);
    return data;
  },

  updateTrack: async (
    trackId: string,
    updates: { title?: string; is_favorite?: boolean }
  ): Promise<Track> => {
    const { data } = await client.patch<Track>(`/tracks/${trackId}`, null, {
      params: updates,
    });
    return data;
  },

  deleteTrack: async (trackId: string): Promise<void> => {
    await client.delete(`/tracks/${trackId}`);
  },

  // System
  health: async () => {
    const { data } = await client.get("/health");
    return data;
  },

  gpuStatus: async () => {
    const { data } = await client.get("/gpu-status");
    return data;
  },
};
