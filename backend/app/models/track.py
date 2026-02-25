import uuid
from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Track(SQLModel, table=True):
    __tablename__ = "tracks"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    title: str
    prompt: str
    tags: Optional[str] = None
    file_path: str
    duration_ms: int
    peaks_json: Optional[str] = None  # JSON array of floats for waveform
    format: str = Field(default="mp3")
    model_used: str = Field(default="ace-step")
    is_favorite: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
