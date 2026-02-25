from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # App
    app_name: str = "TIO Music Studio"
    debug: bool = False

    # Paths
    base_dir: Path = Path(__file__).resolve().parent.parent
    output_dir: Path = base_dir / "outputs"
    data_dir: Path = base_dir / "data"
    models_dir: Path = base_dir / "models"

    # Database
    database_url: str = f"sqlite:///{base_dir / 'data' / 'tio_music.db'}"

    # Redis
    redis_url: str = "redis://localhost:6379/0"
    redis_result_backend: str = "redis://localhost:6379/1"

    # Models
    default_model: str = "ace-step"
    max_vram_gb: float = 22.0  # Reserve 2GB overhead on 24GB GPU

    # Audio
    default_sample_rate: int = 44100
    default_format: str = "mp3"
    mp3_bitrate: str = "320k"

    # LLM
    anthropic_api_key: str = ""
    anthropic_model: str = "claude-sonnet-4-5-20250929"
    ollama_url: str = "http://localhost:11434"
    ollama_model: str = "qwen3:8b"
    use_local_llm: bool = False

    # Generation defaults
    default_duration_seconds: int = 120
    max_duration_seconds: int = 600
    default_inference_steps: int = 8
    default_guidance_scale: float = 3.0

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()

# Ensure directories exist
settings.output_dir.mkdir(parents=True, exist_ok=True)
settings.data_dir.mkdir(parents=True, exist_ok=True)
