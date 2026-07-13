from sqlalchemy import Column, DateTime, Integer, String, Text, UniqueConstraint
from sqlalchemy.sql import func

from app.db.session import Base


class NewsItem(Base):
    """Persisted news/disclosure link discovered from official and public sources."""

    __tablename__ = "news_items"
    __table_args__ = (UniqueConstraint("url_hash", name="uq_news_url_hash"),)

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, nullable=True, index=True)
    company_name = Column(String, nullable=True)
    title = Column(String, nullable=False)
    url = Column(Text, nullable=False)
    url_hash = Column(String, nullable=False, index=True)
    published_at = Column(String, nullable=True, index=True)
    source = Column(String, nullable=False)
    source_type = Column(String, nullable=False, index=True)
    category = Column(String, nullable=False, index=True)
    topic = Column(String, nullable=False)
    summary = Column(Text, nullable=True)
    discovered_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
