from datetime import timedelta

from celery import Celery
from core.config import settings
from core.tasks.update_tasks import update_all_product_prices
from celery.schedules import crontab


TIMESTAMP_DAY = 1
TIMESTAMP_HOUR = TIMESTAMP_DAY * 24
TIMESTAMP_MINUT = TIMESTAMP_HOUR * 60
TIMESTAMP_SECOND = TIMESTAMP_MINUT * 60

celery_app = Celery("price_monitoring", broker=settings.CELERY_BROKER_URL)

celery_app.conf.update(
    result_backend=settings.CELERY_RESULT_BACKEND,
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

celery_app.conf.beat_schedule = {
    "update-prices-every-minute": {
        "task": "core.tasks.update_tasks.update_all_product_prices",  # Указываем полный путь
        "schedule": timedelta(seconds=TIMESTAMP_SECOND),
    },
}

celery_app.autodiscover_tasks(["core.tasks"])
