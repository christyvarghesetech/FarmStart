from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database import Base

class Farmer(Base):
    __tablename__ = "farmers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=True, default="Farmer")
    location = Column(String(100), nullable=False) # District / Taluk
    preferred_language = Column(String(20), nullable=False, default="en") # en, ml
    phone = Column(String(20), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
