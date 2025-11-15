from celery import Celery

from app.core.config import get_settings

settings = get_settings()

celery_app = Celery(
    "doc_insights",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
)

celery_app.conf.update(
    task_routes={"app.workers.tasks.*": {"queue": "documents"}},
    task_track_started=True,
)

celery_app.autodiscover_tasks(["app.workers"])


