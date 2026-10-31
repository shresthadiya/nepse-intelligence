from sqlalchemy import (
    Column,
    Integer,
    Date,
    Float,
    ForeignKey,
    UniqueConstraint,
    Index
)
from sqlalchemy.orm import relationship

from app.database import Base


class StockPrice(Base):

    __tablename__ = "stock_prices"

    id = Column(Integer, primary_key=True, index=True)

    company_id = Column(
        Integer,
        ForeignKey("companies.id", ondelete="CASCADE"),
        nullable=False
    )

    date = Column(Date, nullable=False)

    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)

    volume = Column(Integer, nullable=False)

    company = relationship("Company", backref="stock_prices")

    __table_args__ = (
        UniqueConstraint(
            "company_id",
            "date",
            name="uq_company_stock_date"
        ),
        Index("ix_stock_prices_company_date", "company_id", "date"),
    )