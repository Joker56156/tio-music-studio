import { useState, useCallback } from "react";
import WavesurferPlayer from "@wavesurfer/react";
import type WaveSurfer from "wavesurfer.js";
import { Play, Pause } from "lucide-react";
import { formatDuration } from "../lib/utils";

interface TrackPlayerProps {
  audioUrl: string;
  peaks?: number[] | null;
  compact?: boolean;
}

export function TrackPlayer({ audioUrl, peaks, compact = false }: TrackPlayerProps) {
  const [ws, setWs] = useState<WaveSurfer | null>(null);
  const [playing, setPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);

  const onReady = useCallback((wavesurfer: WaveSurfer) => {
    setWs(wavesurfer);
    setDuration(wavesurfer.getDuration() * 1000);
  }, []);

  const onTimeUpdate = useCallback((time: number) => {
    setCurrentTime(time * 1000);
  }, []);

  return (
    <div className="rounded-lg bg-zinc-900 p-4">
      <WavesurferPlayer
        height={compact ? 40 : 64}
        waveColor="#6d28d9"
        progressColor="#a78bfa"
        cursorColor="#e2e8f0"
        barWidth={2}
        barGap={1}
        barRadius={2}
        url={audioUrl}
        peaks={peaks ? [peaks] : undefined}
        normalize={true}
        onReady={onReady}
        onPlay={() => setPlaying(true)}
        onPause={() => setPlaying(false)}
        onTimeupdate={onTimeUpdate}
      />
      <div className="mt-2 flex items-center gap-3">
        <button
          onClick={() => ws?.playPause()}
          className="flex h-8 w-8 items-center justify-center rounded-full bg-violet-600 text-white hover:bg-violet-500 transition-colors"
        >
          {playing ? <Pause size={14} /> : <Play size={14} className="ml-0.5" />}
        </button>
        <span className="text-xs text-zinc-400 font-mono">
          {formatDuration(currentTime)} / {formatDuration(duration)}
        </span>
      </div>
    </div>
  );
}
