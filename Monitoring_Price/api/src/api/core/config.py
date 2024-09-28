import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Price Monitoring API"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/price_monitoring")

    class Config:
        env_file = ".env"

settings = Settings()
