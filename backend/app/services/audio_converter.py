import os
import logging

from pydub import AudioSegment

from ..config import settings

logger = logging.getLogger(__name__)


def convert_wav_to_mp3(wav_path: str, output_path: str | None = None) -> str:
    if output_path is None:
        output_path = wav_path.rsplit(".", 1)[0] + ".mp3"

    audio = AudioSegment.from_wav(wav_path)
    audio.export(output_path, format="mp3", bitrate=settings.mp3_bitrate)

    logger.info(f"Converted {wav_path} -> {output_path}")
    return output_path


def convert_wav_to_flac(wav_path: str, output_path: str | None = None) -> str:
    if output_path is None:
        output_path = wav_path.rsplit(".", 1)[0] + ".flac"

    audio = AudioSegment.from_wav(wav_path)
    audio.export(output_path, format="flac")

    logger.info(f"Converted {wav_path} -> {output_path}")
    return output_path


def get_audio_duration_ms(file_path: str) -> int:
    audio = AudioSegment.from_file(file_path)
    return len(audio)
