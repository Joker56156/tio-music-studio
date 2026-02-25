import { useState } from "react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { Music } from "lucide-react";
import { GenerationPanel } from "./components/GenerationPanel";
import { TrackLibrary } from "./components/TrackLibrary";
import { TrackPlayer } from "./components/TrackPlayer";
import { GpuStatus } from "./components/GpuStatus";
import type { Track } from "./types/api";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5000,
      retry: 1,
    },
  },
});

function AppContent() {
  const [selectedTrack, setSelectedTrack] = useState<Track | null>(null);

  return (
    <div className="flex h-screen flex-col bg-zinc-950 text-zinc-100">
      {/* Header */}
      <header className="flex items-center justify-between border-b border-zinc-800 px-4 py-3">
        <div className="flex items-center gap-2">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-violet-600">
            <Music size={16} />
          </div>
          <h1 className="text-lg font-bold tracking-tight">TIO Music Studio</h1>
        </div>
        <GpuStatus />
      </header>

      {/* Main Content */}
      <div className="flex flex-1 overflow-hidden">
        {/* Sidebar - Track Library */}
        <aside className="w-64 shrink-0 border-r border-zinc-800 overflow-hidden">
          <TrackLibrary
            onSelectTrack={setSelectedTrack}
            selectedTrackId={selectedTrack?.id}
          />
        </aside>

        {/* Center - Generation Panel */}
        <main className="flex flex-1 flex-col overflow-y-auto p-6">
          <div className="mx-auto w-full max-w-2xl">
            <GenerationPanel />

            {/* Selected Track Player */}
            {selectedTrack && (
              <div className="mt-6">
                <h3 className="mb-2 text-sm font-medium text-zinc-400">
                  {selectedTrack.title}
                </h3>
                <TrackPlayer
                  audioUrl={selectedTrack.audio_url}
                  peaks={selectedTrack.peaks}
                />
              </div>
            )}
          </div>
        </main>
      </div>

      {/* Bottom Player Bar */}
      {selectedTrack && (
        <div className="border-t border-zinc-800 bg-zinc-900 px-4 py-3">
          <div className="mx-auto flex max-w-4xl items-center gap-4">
            <div className="min-w-0 flex-1">
              <p className="truncate text-sm font-medium">{selectedTrack.title}</p>
              <p className="truncate text-xs text-zinc-500">
                {selectedTrack.model_used} · {selectedTrack.tags}
              </p>
            </div>
            <TrackPlayer
              audioUrl={selectedTrack.audio_url}
              peaks={selectedTrack.peaks}
              compact
            />
          </div>
        </div>
      )}
    </div>
  );
}

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AppContent />
    </QueryClientProvider>
  );
}
