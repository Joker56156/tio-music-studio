import { Cpu } from "lucide-react";
import { useGpuStatus } from "../hooks/useGeneration";

export function GpuStatus() {
  const { data: gpu } = useGpuStatus();

  if (!gpu) return null;

  return (
    <div className="flex items-center gap-2 rounded-lg border border-zinc-800 bg-zinc-900 px-3 py-1.5 text-xs">
      <Cpu size={12} className={gpu.available ? "text-green-400" : "text-zinc-500"} />
      {gpu.available ? (
        <>
          <span className="text-zinc-400">{gpu.name}</span>
          <span className="text-zinc-600">|</span>
          <span className="text-zinc-400">
            {gpu.allocated_memory_gb}GB / {gpu.total_memory_gb}GB
          </span>
        </>
      ) : (
        <span className="text-zinc-500">No GPU</span>
      )}
    </div>
  );
}
