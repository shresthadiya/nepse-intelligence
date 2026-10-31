from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey
)
from sqlalchemy.sql import func
from app.database import Base

class CategorizationCorrection(Base):
    __tablename__ = "categorization_corrections"

    id = Column(Integer, primary_key=True, index=True)

    news_id = Column(
        Integer,
        ForeignKey("news.id"),
        nullable=False
    )

    analyst_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    action = Column(String(20), nullable=False)

    company_id = Column(
        Integer,
        ForeignKey("companies.id"),
        nullable=False
    )

    old_confidence = Column(Float, nullable=True)
    new_confidence = Column(Float, nullable=True)

    corrected_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )