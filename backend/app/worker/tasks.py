import os
import logging

from .celery_app import celery_app

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, name="app.worker.tasks.generate_with_ace_step")
def generate_with_ace_step(self, tags: str, lyrics: str, duration: int, seed: int = -1,
                           guidance_scale: float = 3.0, num_inference_steps: int = 8):
    """Generate audio using ACE-Step 1.5."""
    import torch
    import soundfile as sf
    from pydub import AudioSegment

    from ..config import settings
    from ..services.model_manager import model_manager
    from ..services.peaks_generator import generate_peaks

    self.update_state(state="PROCESSING", meta={"progress": 5, "stage": "loading_model"})

    model = model_manager.get_model("ace-step")

    self.update_state(state="PROCESSING", meta={"progress": 20, "stage": "generating"})

    with torch.inference_mode():
        audio = model.generate(
            tags=tags,
            lyrics=lyrics,
            duration=duration,
            num_inference_steps=num_inference_steps,
            guidance_scale=guidance_scale,
            seed=seed,
        )

    self.update_state(state="PROCESSING", meta={"progress": 85, "stage": "saving"})

    # Save WAV
    output_dir = str(settings.output_dir)
    wav_path = os.path.join(output_dir, f"{self.request.id}.wav")
    sf.write(wav_path, audio, samplerate=settings.default_sample_rate)

    # Convert to MP3
    mp3_path = os.path.join(output_dir, f"{self.request.id}.mp3")
    AudioSegment.from_wav(wav_path).export(mp3_path, format="mp3", bitrate=settings.mp3_bitrate)

    # Clean up WAV
    os.remove(wav_path)

    # Generate waveform peaks
    peaks = generate_peaks(mp3_path)

    duration_ms = int(len(audio) / settings.default_sample_rate * 1000)

    return {"file_path": mp3_path, "peaks": peaks, "duration_ms": duration_ms}


@celery_app.task(bind=True, name="app.worker.tasks.generate_with_yue")
def generate_with_yue(self, genre_tags: str, lyrics: str, num_segments: int = 2):
    """Generate audio with premium vocals using YuE."""
    from ..services.model_manager import model_manager

    self.update_state(state="PROCESSING", meta={"progress": 5, "stage": "loading_yue"})

    # Evict other models — YuE needs ~20GB VRAM
    model_manager.evict_all()

    self.update_state(state="PROCESSING", meta={"progress": 15, "stage": "stage1_inference"})

    model = model_manager.get_model("yue")

    # Stage 1: 7B model generates audio tokens from lyrics
    # Stage 2: 1B model reconstructs residual tokens
    self.update_state(state="PROCESSING", meta={"progress": 70, "stage": "stage2_inference"})

    # TODO: Wire actual YuE inference pipeline
    # For now, placeholder that will be replaced in Phase 2B
    raise NotImplementedError("YuE integration pending — complete in Phase 2B session")


@celery_app.task(bind=True, name="app.worker.tasks.generate_with_diffrhythm")
def generate_with_diffrhythm(self, tags: str, lyrics: str, duration: int):
    """Generate fast instrumental variations using DiffRhythm."""
    from ..services.model_manager import model_manager

    self.update_state(state="PROCESSING", meta={"progress": 5, "stage": "loading_diffrhythm"})

    model = model_manager.get_model("diffrhythm")

    self.update_state(state="PROCESSING", meta={"progress": 20, "stage": "generating"})

    # TODO: Wire actual DiffRhythm inference pipeline
    # For now, placeholder that will be replaced in Phase 2C session
    raise NotImplementedError("DiffRhythm integration pending — complete in Phase 2C session")
