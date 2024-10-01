from celery import Celery
from core.config import settings
from core.tasks.update_tasks import update_all_product_prices

# Создаем новый экземпляр Celery
celery_app = Celery('price_monitoring', broker=settings.CELERY_BROKER_URL)

# Настройки Celery
celery_app.conf.update(
    result_backend=settings.CELERY_RESULT_BACKEND,
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

# Подключаем Beat расписание задач
from celery.schedules import crontab

celery_app.conf.beat_schedule = {
    'update-prices-every-minute': {
        'task': 'core.tasks.update_tasks.update_all_product_prices',  # Указываем полный путь
        'schedule': crontab(minute='*/1'),  # Каждую минуту
    },
}

# Регистрируем задачи
celery_app.autodiscover_tasks(['core.tasks'])
