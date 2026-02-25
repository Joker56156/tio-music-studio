export interface GenerationRequest {
  description: string;
  lyrics?: string;
  duration_seconds?: number;
  model?: "ace-step" | "yue" | "diffrhythm";
  instrumental?: boolean;
  vocal_priority?: "standard" | "premium";
  seed?: number;
  guidance_scale?: number;
  num_inference_steps?: number;
}

export interface GenerateResponse {
  job_id: string;
  task_id: string;
  status: string;
  structured_prompt?: Record<string, unknown>;
}

export interface TaskStatus {
  task_id: string;
  status: "PENDING" | "STARTED" | "PROCESSING" | "SUCCESS" | "FAILURE";
  progress: number;
  stage?: string;
  result?: {
    file_path: string;
    peaks: number[];
    duration_ms: number;
  };
  error?: string;
}

export interface Track {
  id: string;
  title: string;
  prompt: string;
  tags: string;
  audio_url: string;
  peaks: number[] | null;
  duration_ms: number;
  model_used: string;
  format: string;
  is_favorite: boolean;
  created_at: string;
}
