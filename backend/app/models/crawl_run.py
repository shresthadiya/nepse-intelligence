from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.sql import func

from app.database import Base


class CrawlRun(Base):
    __tablename__ = "crawl_runs"

    id = Column(Integer, primary_key=True, index=True)

    status = Column(
        String(30),
        nullable=False,
        default="pending",
        index=True
    )

    started_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    completed_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    total_fetched = Column(Integer, default=0)
    total_inserted = Column(Integer, default=0)
    total_duplicates = Column(Integer, default=0)
    total_categorized = Column(Integer, default=0)
    total_uncategorized = Column(Integer, default=0)
    total_failed = Column(Integer, default=0)

    results = Column(JSON, nullable=True)

    error_message = Column(String(2000), nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )