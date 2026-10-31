from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base


class Company(Base):

    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)

    symbol = Column(
        String(20),
        unique=True,
        nullable=False,
        index=True
    )

    name = Column(String(150), nullable=False)

    sector = Column(String(100), nullable=True)

    is_active = Column(Boolean, default=True)