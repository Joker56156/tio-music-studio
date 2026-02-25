import uuid
from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class GenerationJob(SQLModel, table=True):
    __tablename__ = "generation_jobs"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    prompt: str
    tags: Optional[str] = None
    lyrics: Optional[str] = None
    model_used: str = Field(default="ace-step")
    status: str = Field(default="pending")  # pending/processing/completed/failed
    progress: float = Field(default=0.0)
    celery_task_id: Optional[str] = None
    file_path: Optional[str] = None
    duration_ms: Optional[int] = None
    error_message: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
