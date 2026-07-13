from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List

from sqlalchemy.orm import Session

from app.models.news_model import NewsItem
from app.models.snapshot_model import DailySnapshot


def snapshot_exists_for_date(db: Session, date_str: str) -> bool:
    """Check whether any snapshot row exists for the given ISO date"""
    return (
        db.query(DailySnapshot.id).filter(DailySnapshot.date == date_str).first()
        is not None
    )


def bulk_insert_snapshots(db: Session, date_str: str, rows: List[Dict[str, Any]]) -> None:
    """Insert one DailySnapshot row per stock for the given date"""
    db.bulk_save_objects(
        [
            DailySnapshot(
                symbol=row["symbol"],
                date=date_str,
                price=row["price"],
                change=row["change"],
                volume=row["volume"],
                market_cap=row.get("market_cap"),
            )
            for row in rows
        ]
    )
    db.commit()


def get_symbol_history(db: Session, symbol: str, days: int) -> List[DailySnapshot]:
    """Get up to `days` most recent snapshots for a symbol, oldest first"""
    cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%d")
    rows = (
        db.query(DailySnapshot)
        .filter(DailySnapshot.symbol == symbol, DailySnapshot.date >= cutoff)
        .order_by(DailySnapshot.date.asc())
        .all()
    )
    return rows


def get_snapshots_in_range(db: Session, days: int) -> List[DailySnapshot]:
    """Get all snapshot rows (all symbols) within the last `days` days, oldest first"""
    cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%d")
    rows = (
        db.query(DailySnapshot)
        .filter(DailySnapshot.date >= cutoff)
        .order_by(DailySnapshot.date.asc())
        .all()
    )
    return rows


def upsert_news_items(db: Session, items: List[Dict[str, Any]]) -> int:
    """Insert news items by URL hash, updating lightweight metadata on duplicates."""
    inserted = 0
    seen_hashes = set()
    for item in items:
        url_hash = item["url_hash"]
        if url_hash in seen_hashes:
            continue
        seen_hashes.add(url_hash)

        existing = (
            db.query(NewsItem)
            .filter(NewsItem.url_hash == url_hash)
            .first()
        )
        if existing:
            existing.title = item.get("title", existing.title)
            existing.published_at = item.get("published_at") or existing.published_at
            existing.summary = item.get("summary") or existing.summary
            existing.category = item.get("category", existing.category)
            existing.topic = item.get("topic", existing.topic)
            continue

        db.add(NewsItem(**item))
        inserted += 1

    db.commit()
    return inserted


def get_news_items(
    db: Session,
    limit: int = 80,
    symbol: str | None = None,
    source_type: str | None = None,
    category: str | None = None,
) -> List[NewsItem]:
    """Get latest persisted news, optionally filtered by stock/source/category."""
    query = db.query(NewsItem)
    if symbol:
        query = query.filter(NewsItem.symbol == symbol.upper())
    if source_type:
        query = query.filter(NewsItem.source_type == source_type)
    if category:
        query = query.filter(NewsItem.category == category)

    return (
        query.order_by(NewsItem.published_at.desc(), NewsItem.discovered_at.desc())
        .limit(limit)
        .all()
    )
