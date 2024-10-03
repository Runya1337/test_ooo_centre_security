import os
from pydantic_settings import BaseSettings
from typing import ClassVar


class Settings(BaseSettings):
    TELEGRAM_TOKEN: ClassVar[str] = "7629046050:AAGFrmvDJW4WDJ0gVBs-2qhDEhmep4TU47s"

    class Config:
        env_file = ".env"


settings = Settings()
