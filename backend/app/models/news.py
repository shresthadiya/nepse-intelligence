from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    UniqueConstraint
)
from sqlalchemy.sql import func
from app.database import Base

class News(Base):

    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    headline = Column(String(500), nullable=False)
    body = Column(Text, nullable=True)
    source = Column(String(150), nullable=False)
    url = Column(String(1000), unique=True, nullable=False)
    published_at = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )