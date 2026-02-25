import gc
import time
import logging
from typing import Any

logger = logging.getLogger(__name__)

# Estimated VRAM usage per model (in bytes)
MODEL_VRAM_ESTIMATES = {
    "ace-step": 4 * 1024**3,       # ~4 GB
    "yue": 20 * 1024**3,           # ~20 GB (7B + 1B stages)
    "diffrhythm": 8 * 1024**3,     # ~8 GB
}


class ModelManager:
    def __init__(self, max_vram_gb: float = 22.0):
        self.loaded_models: dict[str, dict[str, Any]] = {}
        self.max_vram = max_vram_gb * 1024**3

    def get_model(self, name: str):
        if name not in self.loaded_models:
            self._evict_lru_if_needed(name)
            self._load_model(name)
        self.loaded_models[name]["last_used"] = time.time()
        return self.loaded_models[name]["model"]

    def _load_model(self, name: str):
        logger.info(f"Loading model: {name}")

        if name == "ace-step":
            model = self._load_ace_step()
        elif name == "yue":
            model = self._load_yue()
        elif name == "diffrhythm":
            model = self._load_diffrhythm()
        else:
            raise ValueError(f"Unknown model: {name}")

        self.loaded_models[name] = {
            "model": model,
            "last_used": time.time(),
            "vram_estimate": MODEL_VRAM_ESTIMATES.get(name, 0),
        }
        logger.info(f"Model {name} loaded successfully")

    def _load_ace_step(self):
        """Load ACE-Step 1.5 model."""
        # TODO: Replace with actual ACE-Step loading in Phase 2A
        # The actual implementation will:
        # 1. Import from models/ace-step
        # 2. Load DiT, VAE, text encoder, and LM planner
        # 3. Move to CUDA with torch.inference_mode()
        logger.warning("ACE-Step stub loaded — replace in Phase 2A")

        class ACEStepStub:
            def generate(self, tags, lyrics, duration, num_inference_steps=8,
                         guidance_scale=3.0, seed=-1):
                import numpy as np
                # Return silence as placeholder
                samples = int(duration * 44100)
                return np.zeros(samples, dtype=np.float32)

        return ACEStepStub()

    def _load_yue(self):
        """Load YuE model (Stage 1 + Stage 2)."""
        # TODO: Replace with actual YuE loading in Phase 2B
        logger.warning("YuE stub loaded — replace in Phase 2B")
        raise NotImplementedError("YuE loading not yet implemented")

    def _load_diffrhythm(self):
        """Load DiffRhythm model."""
        # TODO: Replace with actual DiffRhythm loading in Phase 2C
        logger.warning("DiffRhythm stub loaded — replace in Phase 2C")
        raise NotImplementedError("DiffRhythm loading not yet implemented")

    def _evict_lru_if_needed(self, incoming: str):
        needed = MODEL_VRAM_ESTIMATES.get(incoming, 0)
        while self._used_vram() + needed > self.max_vram and self.loaded_models:
            lru_name = min(
                self.loaded_models,
                key=lambda k: self.loaded_models[k]["last_used"],
            )
            logger.info(f"Evicting model {lru_name} to free VRAM")
            self._unload_model(lru_name)

    def _unload_model(self, name: str):
        if name in self.loaded_models:
            del self.loaded_models[name]["model"]
            del self.loaded_models[name]
            gc.collect()
            try:
                import torch
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
            except ImportError:
                pass

    def _used_vram(self) -> float:
        return sum(m["vram_estimate"] for m in self.loaded_models.values())

    def _free_vram(self) -> float:
        return self.max_vram - self._used_vram()

    def evict_all(self):
        for name in list(self.loaded_models.keys()):
            self._unload_model(name)


# Singleton instance
model_manager = ModelManager()
