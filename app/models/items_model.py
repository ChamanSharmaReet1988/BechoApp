from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text, Enum
from app.database.base import Base
from datetime import datetime


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    userId = Column(Integer,  nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    price = Column(String(255), nullable=False)
    imageUrls = Column(Text, nullable=True)
    isNegotiable = Column(Boolean, default=False)
    isActive = Column(Boolean, default=True)
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow,
                       onupdate=datetime.utcnow)
    views = Column(Integer, default=0)
    otherDetails = Column(Text, nullable=False)
    isDeleted = Column(Boolean, default=False)
