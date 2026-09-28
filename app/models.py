from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from datetime import datetime, timezone

from app.database import Base


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String(20), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    category = Column(String(100), nullable=True)
    area = Column(String(100), nullable=True)
    instructions = Column(Text, nullable=True)
    image_url = Column(String(500), nullable=True)
    ingredients = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    rating = Column(Float, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
