from sqlalchemy import Column, DateTime, Float, Integer, String, UniqueConstraint
from sqlalchemy.sql import func

from app.db.session import Base


class DailySnapshot(Base):
    """One closing snapshot per stock per trading day, used to build historical charts"""

    __tablename__ = "daily_snapshots"
    __table_args__ = (UniqueConstraint("symbol", "date", name="uq_symbol_date"),)

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, nullable=False, index=True)
    date = Column(String, nullable=False, index=True)  # ISO date string, e.g. "2026-07-12"
    price = Column(Float, nullable=False)
    change = Column(Float, nullable=False)
    volume = Column(Integer, nullable=False)
    market_cap = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
