import { useState } from "react";
import { Music, Heart, Trash2, Star } from "lucide-react";
import { useTracks } from "../hooks/useGeneration";
import { api } from "../lib/api";
import { formatDuration, formatDate } from "../lib/utils";
import type { Track } from "../types/api";
import { useQueryClient } from "@tanstack/react-query";

interface TrackLibraryProps {
  onSelectTrack: (track: Track) => void;
  selectedTrackId?: string;
}

export function TrackLibrary({ onSelectTrack, selectedTrackId }: TrackLibraryProps) {
  const { data: tracks, isLoading } = useTracks();
  const [showFavoritesOnly, setShowFavoritesOnly] = useState(false);
  const qc = useQueryClient();

  const filteredTracks = showFavoritesOnly
    ? tracks?.filter((t) => t.is_favorite)
    : tracks;

  const toggleFavorite = async (track: Track, e: React.MouseEvent) => {
    e.stopPropagation();
    await api.updateTrack(track.id, { is_favorite: !track.is_favorite });
    qc.invalidateQueries({ queryKey: ["tracks"] });
  };

  const deleteTrack = async (track: Track, e: React.MouseEvent) => {
    e.stopPropagation();
    await api.deleteTrack(track.id);
    qc.invalidateQueries({ queryKey: ["tracks"] });
  };

  return (
    <div className="flex h-full flex-col">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-zinc-800 px-3 py-2">
        <h2 className="text-sm font-semibold text-zinc-300">Library</h2>
        <button
          onClick={() => setShowFavoritesOnly(!showFavoritesOnly)}
          className={`rounded p-1 transition-colors ${
            showFavoritesOnly
              ? "text-yellow-400 hover:text-yellow-300"
              : "text-zinc-500 hover:text-zinc-300"
          }`}
        >
          <Star size={14} />
        </button>
      </div>

      {/* Track List */}
      <div className="flex-1 overflow-y-auto">
        {isLoading ? (
          <div className="flex items-center justify-center py-8">
            <div className="h-5 w-5 animate-spin rounded-full border-2 border-violet-500 border-t-transparent" />
          </div>
        ) : filteredTracks?.length === 0 ? (
          <div className="flex flex-col items-center justify-center gap-2 py-8 text-zinc-500">
            <Music size={24} />
            <p className="text-xs">No tracks yet</p>
          </div>
        ) : (
          filteredTracks?.map((track) => (
            <button
              key={track.id}
              onClick={() => onSelectTrack(track)}
              className={`group flex w-full items-center gap-2 border-b border-zinc-800/50 px-3 py-2 text-left transition-colors hover:bg-zinc-800/50 ${
                selectedTrackId === track.id ? "bg-zinc-800" : ""
              }`}
            >
              <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded bg-violet-600/20 text-violet-400">
                <Music size={14} />
              </div>
              <div className="min-w-0 flex-1">
                <p className="truncate text-sm text-zinc-200">{track.title}</p>
                <p className="truncate text-xs text-zinc-500">
                  {track.model_used} · {formatDuration(track.duration_ms)} ·{" "}
                  {formatDate(track.created_at)}
                </p>
              </div>
              <div className="flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                <button
                  onClick={(e) => toggleFavorite(track, e)}
                  className="rounded p-1 hover:bg-zinc-700"
                >
                  <Heart
                    size={12}
                    className={
                      track.is_favorite ? "fill-red-400 text-red-400" : "text-zinc-400"
                    }
                  />
                </button>
                <button
                  onClick={(e) => deleteTrack(track, e)}
                  className="rounded p-1 hover:bg-zinc-700 text-zinc-400 hover:text-red-400"
                >
                  <Trash2 size={12} />
                </button>
              </div>
            </button>
          ))
        )}
      </div>
    </div>
  );
}
