import os
from pydantic_settings import BaseSettings
from typing import ClassVar


class Settings(BaseSettings):
    PROJECT_NAME: str = "Price Monitoring API"
    DATABASE_URL: str = "postgresql://user:password@db:5432/price_monitoring"
    CELERY_BROKER_URL: ClassVar[str] = "redis://redis:6379/0"
    CELERY_RESULT_BACKEND: ClassVar[str] = "redis://redis:6379/0"


settings = Settings()
