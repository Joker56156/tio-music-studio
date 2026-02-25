import { CheckCircle2, XCircle, Loader2 } from "lucide-react";
import type { TaskStatus } from "../types/api";

interface TaskProgressProps {
  task: TaskStatus;
}

export function TaskProgress({ task }: TaskProgressProps) {
  const isComplete = task.status === "SUCCESS";
  const isFailed = task.status === "FAILURE";

  return (
    <div className="rounded-lg border border-zinc-700 bg-zinc-800/50 p-3">
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-2">
          {isComplete ? (
            <CheckCircle2 size={16} className="text-green-400" />
          ) : isFailed ? (
            <XCircle size={16} className="text-red-400" />
          ) : (
            <Loader2 size={16} className="animate-spin text-violet-400" />
          )}
          <span className="text-sm text-zinc-300">
            {isComplete
              ? "Complete"
              : isFailed
                ? "Failed"
                : task.stage ?? "Processing..."}
          </span>
        </div>
        <span className="text-xs font-mono text-zinc-500">
          {Math.round(task.progress)}%
        </span>
      </div>

      {/* Progress bar */}
      <div className="h-1.5 w-full overflow-hidden rounded-full bg-zinc-700">
        <div
          className={`h-full rounded-full transition-all duration-500 ${
            isComplete
              ? "bg-green-500"
              : isFailed
                ? "bg-red-500"
                : "bg-violet-500"
          }`}
          style={{ width: `${task.progress}%` }}
        />
      </div>

      {isFailed && task.error && (
        <p className="mt-2 text-xs text-red-400">{task.error}</p>
      )}
    </div>
  );
}
