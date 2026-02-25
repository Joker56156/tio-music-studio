import { useState } from "react";
import { Wand2, Music, Mic } from "lucide-react";
import { useGenerateMusic, useTaskStatus } from "../hooks/useGeneration";
import { TaskProgress } from "./TaskProgress";
import type { GenerationRequest } from "../types/api";

const MODEL_OPTIONS = [
  { value: "ace-step" as const, label: "ACE-Step 1.5", description: "Fast + versatile (default)" },
  { value: "yue" as const, label: "YuE", description: "Premium vocals (slower)" },
  { value: "diffrhythm" as const, label: "DiffRhythm", description: "Fast instrumentals" },
];

export function GenerationPanel() {
  const [description, setDescription] = useState("");
  const [lyrics, setLyrics] = useState("");
  const [showLyrics, setShowLyrics] = useState(false);
  const [duration, setDuration] = useState(120);
  const [model, setModel] = useState<GenerationRequest["model"]>(undefined);
  const [activeTaskId, setActiveTaskId] = useState<string | null>(null);

  const generateMutation = useGenerateMusic();
  const taskStatus = useTaskStatus(activeTaskId);

  const handleGenerate = () => {
    if (!description.trim()) return;

    generateMutation.mutate(
      {
        description: description.trim(),
        lyrics: showLyrics && lyrics.trim() ? lyrics.trim() : undefined,
        duration_seconds: duration,
        model,
        instrumental: !showLyrics,
      },
      {
        onSuccess: (response) => {
          setActiveTaskId(response.task_id);
        },
      }
    );
  };

  const isGenerating =
    generateMutation.isPending ||
    (activeTaskId &&
      taskStatus.data?.status !== "SUCCESS" &&
      taskStatus.data?.status !== "FAILURE");

  return (
    <div className="flex flex-col gap-4">
      {/* Description Input */}
      <div>
        <label className="mb-1.5 block text-sm font-medium text-zinc-300">
          Describe your song
        </label>
        <textarea
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="dark hypnotic phonk with distorted bass and chopped vocal samples..."
          className="h-28 w-full resize-none rounded-lg border border-zinc-700 bg-zinc-800 px-3 py-2 text-sm text-zinc-100 placeholder:text-zinc-500 focus:border-violet-500 focus:outline-none focus:ring-1 focus:ring-violet-500"
        />
      </div>

      {/* Lyrics Toggle & Input */}
      <div>
        <button
          onClick={() => setShowLyrics(!showLyrics)}
          className="flex items-center gap-2 text-sm text-zinc-400 hover:text-zinc-200 transition-colors"
        >
          <Mic size={14} />
          {showLyrics ? "Hide lyrics" : "Add lyrics"}
        </button>
        {showLyrics && (
          <textarea
            value={lyrics}
            onChange={(e) => setLyrics(e.target.value)}
            placeholder={"[Verse 1]\nYour lyrics here...\n\n[Chorus]\n..."}
            className="mt-2 h-32 w-full resize-none rounded-lg border border-zinc-700 bg-zinc-800 px-3 py-2 text-sm text-zinc-100 placeholder:text-zinc-500 focus:border-violet-500 focus:outline-none focus:ring-1 focus:ring-violet-500 font-mono"
          />
        )}
      </div>

      {/* Controls Row */}
      <div className="flex flex-wrap items-end gap-4">
        {/* Duration */}
        <div className="flex-1 min-w-[140px]">
          <label className="mb-1.5 block text-xs text-zinc-400">
            Duration: {duration}s
          </label>
          <input
            type="range"
            min={10}
            max={300}
            step={10}
            value={duration}
            onChange={(e) => setDuration(Number(e.target.value))}
            className="w-full accent-violet-500"
          />
        </div>

        {/* Model Selector */}
        <div className="flex-1 min-w-[160px]">
          <label className="mb-1.5 block text-xs text-zinc-400">Model</label>
          <select
            value={model ?? ""}
            onChange={(e) =>
              setModel(
                (e.target.value || undefined) as GenerationRequest["model"]
              )
            }
            className="w-full rounded-lg border border-zinc-700 bg-zinc-800 px-3 py-2 text-sm text-zinc-100 focus:border-violet-500 focus:outline-none"
          >
            <option value="">Auto-select</option>
            {MODEL_OPTIONS.map((opt) => (
              <option key={opt.value} value={opt.value}>
                {opt.label} — {opt.description}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Generate Button */}
      <button
        onClick={handleGenerate}
        disabled={!description.trim() || !!isGenerating}
        className="flex items-center justify-center gap-2 rounded-lg bg-violet-600 px-6 py-3 text-sm font-semibold text-white transition-colors hover:bg-violet-500 disabled:cursor-not-allowed disabled:opacity-50"
      >
        {isGenerating ? (
          <>
            <Music size={16} className="animate-pulse" />
            Generating...
          </>
        ) : (
          <>
            <Wand2 size={16} />
            Generate
          </>
        )}
      </button>

      {/* Task Progress */}
      {activeTaskId && taskStatus.data && (
        <TaskProgress task={taskStatus.data} />
      )}
    </div>
  );
}
