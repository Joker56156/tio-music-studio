from celery import Celery

from ..config import settings

celery_app = Celery("tio_music")
celery_app.conf.update(
    broker_url=settings.redis_url,
    result_backend=settings.redis_result_backend,
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    task_track_started=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    task_time_limit=600,  # 10 min hard limit
    task_soft_time_limit=540,  # 9 min soft limit
)

# Auto-discover tasks
celery_app.autodiscover_tasks(["app.worker"])
