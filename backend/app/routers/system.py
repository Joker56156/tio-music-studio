import platform

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health():
    return {"status": "ok", "version": "0.1.0"}


@router.get("/gpu-status")
async def gpu_status():
    try:
        import torch

        if torch.cuda.is_available():
            device = torch.cuda.get_device_properties(0)
            return {
                "available": True,
                "name": device.name,
                "total_memory_gb": round(device.total_mem / 1024**3, 1),
                "allocated_memory_gb": round(torch.cuda.memory_allocated(0) / 1024**3, 2),
                "reserved_memory_gb": round(torch.cuda.memory_reserved(0) / 1024**3, 2),
                "cuda_version": torch.version.cuda,
                "pytorch_version": torch.__version__,
            }
        else:
            return {"available": False, "reason": "CUDA not available"}
    except ImportError:
        return {"available": False, "reason": "PyTorch not installed"}


@router.get("/system-info")
async def system_info():
    return {
        "platform": platform.system(),
        "python_version": platform.python_version(),
        "architecture": platform.machine(),
    }
