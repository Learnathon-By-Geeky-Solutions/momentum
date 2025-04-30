from app.tasks import celery_app

celery_app.autodiscover_tasks(["app"])
