from typing import Optional, Literal

from pydantic import BaseModel, Field


class GenerateRequest(BaseModel):
    description: str = Field(..., min_length=1, max_length=2000)
    lyrics: Optional[str] = None
    duration_seconds: int = Field(default=120, ge=10, le=600)
    model: Optional[Literal["ace-step", "yue", "diffrhythm"]] = None
    instrumental: bool = False
    vocal_priority: Optional[Literal["standard", "premium"]] = "standard"
    seed: int = Field(default=-1)
    guidance_scale: float = Field(default=3.0, ge=1.0, le=15.0)
    num_inference_steps: int = Field(default=8, ge=4, le=100)


class GenerateResponse(BaseModel):
    job_id: str
    task_id: str
    status: str
    structured_prompt: Optional[dict] = None


class TaskStatus(BaseModel):
    task_id: str
    status: str  # PENDING, STARTED, PROCESSING, SUCCESS, FAILURE
    progress: float = 0.0
    stage: Optional[str] = None
    result: Optional[dict] = None
    error: Optional[str] = None
