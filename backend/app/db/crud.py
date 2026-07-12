from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List

from sqlalchemy.orm import Session

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
