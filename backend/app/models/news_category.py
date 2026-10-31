from sqlalchemy import (
    Column,
    Integer,
    Float,
    ForeignKey,
    UniqueConstraint
)

from sqlalchemy.orm import relationship
from app.database import Base

class NewsCategory(Base):
    __tablename__ = "news_categories"

    id = Column(Integer, primary_key=True, index=True)

    news_id = Column(
        Integer,
        ForeignKey("news.id", ondelete="CASCADE"),
        nullable=False
    )

    company_id = Column(
        Integer,
        ForeignKey("companies.id", ondelete="CASCADE"),
        nullable=False
    )

    confidence = Column(Float, nullable=False)
    news = relationship("News", backref="categories")
    company = relationship("Company")

    __table_args__ = (
        UniqueConstraint(
            "news_id",
            "company_id",
            name="uq_news_company"
        ),
    )