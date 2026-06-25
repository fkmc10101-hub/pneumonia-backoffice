from pydantic_settings import BaseSettings
from pydantic import computed_field
import os
from pathlib import Path

class Settings(BaseSettings):
    DB_USER: str = "root"
    DB_PASSWORD: str = ""  # .env에서 주입 (Git에 올리지 않음)
    DB_HOST: str = "localhost"
    DB_PORT: str = "3306"
    DB_NAME: str = "ai_health"
    DB_SSL: bool = False  # 클라우드 DB(Aiven 등) 접속 시 .env에서 true

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        url = f"mysql+asyncmy://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        return url + "?ssl-mode=REQUIRED" if self.DB_SSL else url

    model_config = {
        "env_file": str(Path(__file__).resolve().parent.parent.parent / ".env"),
        "extra": "ignore"
    }

settings = Settings()
