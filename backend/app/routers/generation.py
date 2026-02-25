import json

from celery.result import AsyncResult
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from ..database import get_session
from ..models.job import GenerationJob
from ..schemas.generation import GenerateRequest, GenerateResponse, TaskStatus
from ..services.router import select_model
from ..worker.celery_app import celery_app
from ..worker.tasks import generate_with_ace_step, generate_with_yue, generate_with_diffrhythm

router = APIRouter()


@router.post("/generate", response_model=GenerateResponse)
async def generate(request: GenerateRequest, session: Session = Depends(get_session)):
    # Select model based on request
    model = select_model(request)

    # Build tags from description (will be replaced by LLM translator in Phase 4)
    tags = request.description

    # Dispatch to appropriate Celery task
    if model == "ace-step":
        task = generate_with_ace_step.delay(
            tags=tags,
            lyrics=request.lyrics or "[Instrumental]",
            duration=request.duration_seconds,
            seed=request.seed,
            guidance_scale=request.guidance_scale,
            num_inference_steps=request.num_inference_steps,
        )
    elif model == "yue":
        task = generate_with_yue.delay(
            genre_tags=tags,
            lyrics=request.lyrics or "",
        )
    elif model == "diffrhythm":
        task = generate_with_diffrhythm.delay(
            tags=tags,
            lyrics=request.lyrics or "",
            duration=request.duration_seconds,
        )
    else:
        raise HTTPException(status_code=400, detail=f"Unknown model: {model}")

    # Save job to database
    job = GenerationJob(
        prompt=request.description,
        tags=tags,
        lyrics=request.lyrics,
        model_used=model,
        status="pending",
        celery_task_id=task.id,
    )
    session.add(job)
    session.commit()
    session.refresh(job)

    return GenerateResponse(
        job_id=job.id,
        task_id=task.id,
        status="pending",
    )


@router.get("/tasks/{task_id}", response_model=TaskStatus)
async def get_task(task_id: str):
    result = AsyncResult(task_id, app=celery_app)

    progress = 0.0
    stage = None
    error = None
    task_result = None

    if isinstance(result.info, dict):
        progress = result.info.get("progress", 0)
        stage = result.info.get("stage")
    elif result.failed():
        error = str(result.result)

    if result.ready() and result.successful():
        task_result = result.get()
        progress = 100.0

    return TaskStatus(
        task_id=task_id,
        status=result.status,
        progress=progress,
        stage=stage,
        result=task_result,
        error=error,
    )
