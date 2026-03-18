from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings


def _ensure_sqlite_directory_exists(database_url: str) -> None:
    if not database_url.startswith("sqlite") or database_url.endswith(":memory:"):
        return

    _, separator, raw_path = database_url.partition(":///")
    if not separator or not raw_path:
        return

    database_path = raw_path.partition("?")[0]
    Path(database_path).expanduser().resolve().parent.mkdir(parents=True, exist_ok=True)


# Database setup
_ensure_sqlite_directory_exists(settings.database_url)

engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False}
    if "sqlite" in settings.database_url
    else {},
    pool_size=20,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=3600,
    pool_pre_ping=True,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db(db: Session = None):
    """Get database session - can be used as dependency or directly"""
    if db is None:
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
    else:
        yield db
