import json
import logging
import subprocess

logger = logging.getLogger(__name__)


def generate_peaks(audio_path: str, pixels_per_second: int = 10) -> list[float]:
    """Generate waveform peaks using audiowaveform CLI (BBC R&D).

    Falls back to a Python-based approach if audiowaveform is not installed.
    """
    try:
        return _generate_peaks_audiowaveform(audio_path, pixels_per_second)
    except FileNotFoundError:
        logger.warning("audiowaveform not found, using Python fallback")
        return _generate_peaks_python(audio_path, pixels_per_second)


def _generate_peaks_audiowaveform(audio_path: str, pixels_per_second: int) -> list[float]:
    result = subprocess.run(
        [
            "audiowaveform",
            "-i", audio_path,
            "-o", "-",
            "--pixels-per-second", str(pixels_per_second),
            "-b", "8",
            "--output-format", "json",
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    data = json.loads(result.stdout)["data"]
    max_val = max(abs(x) for x in data) or 1
    return [round(x / max_val, 3) for x in data]


def _generate_peaks_python(audio_path: str, pixels_per_second: int) -> list[float]:
    """Python fallback for peak generation using soundfile."""
    import numpy as np
    import soundfile as sf

    audio_data, sample_rate = sf.read(audio_path)

    # Convert stereo to mono
    if audio_data.ndim > 1:
        audio_data = audio_data.mean(axis=1)

    # Calculate samples per pixel
    samples_per_pixel = sample_rate // pixels_per_second

    peaks = []
    for i in range(0, len(audio_data), samples_per_pixel):
        chunk = audio_data[i : i + samples_per_pixel]
        if len(chunk) > 0:
            peaks.append(float(np.max(np.abs(chunk))))

    # Normalize to [-1, 1]
    max_peak = max(peaks) if peaks else 1.0
    if max_peak > 0:
        peaks = [round(p / max_peak, 3) for p in peaks]

    return peaks
