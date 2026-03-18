from pathlib import Path
from typing import List

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


BACKEND_DIR = Path(__file__).resolve().parents[2]
PROJECT_ROOT = BACKEND_DIR.parent
DEFAULT_DATABASE_PATH = BACKEND_DIR / "gse_tracker.db"


def _build_sqlite_url(database_path: Path) -> str:
    return f"sqlite:///{database_path.resolve().as_posix()}"


def _normalize_database_url(database_url: str) -> str:
    if not database_url.startswith("sqlite") or database_url.endswith(":memory:"):
        return database_url

    prefix, separator, raw_path = database_url.partition(":///")
    if not separator or not raw_path:
        return database_url

    database_path, _, query_string = raw_path.partition("?")
    path = Path(database_path)

    if path.is_absolute():
        resolved_path = path
    elif database_path.startswith("./backend/") or database_path.startswith("backend/"):
        resolved_path = (PROJECT_ROOT / database_path.removeprefix("./")).resolve()
    else:
        resolved_path = (BACKEND_DIR / database_path).resolve()

    normalized_url = f"{prefix}:///{resolved_path.as_posix()}"
    if query_string:
        return f"{normalized_url}?{query_string}"

    return normalized_url


class Settings(BaseSettings):
    """Application settings"""

    # Ollama AI
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "phi4-mini:latest"
    ollama_temperature: float = 0.3

    # GSE API
    gse_api_url: str = "https://dev.kwayisi.org/apis/gse"

    # Database
    database_url: str = _build_sqlite_url(DEFAULT_DATABASE_PATH)

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

    @field_validator("database_url", mode="before")
    @classmethod
    def normalize_database_url(cls, value: str) -> str:
        return _normalize_database_url(value)


settings = Settings()
