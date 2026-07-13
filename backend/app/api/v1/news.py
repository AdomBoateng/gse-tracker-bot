from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.news_service import news_service

router = APIRouter(prefix="/api/v1/news", tags=["news"])


@router.get("")
async def get_news(
    symbol: str | None = None,
    source_type: str | None = None,
    category: str | None = None,
    refresh: bool = False,
    db: Session = Depends(get_db),
):
    """Persisted hybrid news from official sources plus Google News RSS."""
    return await news_service.get_news(
        db,
        symbol=symbol,
        source_type=source_type,
        category=category,
        refresh=refresh,
    )
