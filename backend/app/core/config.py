from pathlib import Path
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


BACKEND_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    """Application settings"""

    # Ollama AI
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "phi4-mini:latest"
    ollama_temperature: float = 0.3

    # GSE API
    gse_api_url: str = "https://dev.kwayisi.org/apis/gse"

    # Database (daily snapshots for historical charts)
    database_url: str = "sqlite:///./gse_tracker.db"

    # Application
    debug: bool = True
    port: int = 8000
    app_name: str = "GSE Tracker API"
    app_version: str = "1.0.0"

    # CORS
    cors_origins: List[str] = ["http://localhost:5173", "http://localhost:3000"]

    # Gunicorn (ignored by Pydantic, used directly from .env)
    gunicorn_workers: int = 4
    gunicorn_timeout: int = 120

    model_config = SettingsConfigDict(
        env_file=str(BACKEND_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",  # Ignore extra environment variables
    )


settings = Settings()
