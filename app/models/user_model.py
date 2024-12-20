from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from app.database.base import Base
from datetime import datetime


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(512), nullable=True)  # Full name of the user
    email = Column(String(512), unique=True, nullable=True)  # Email ID
    # Optional phone number
    phone = Column(String(512), unique=True, nullable=False)
    passwordHash = Column(String(512), nullable=True)  # Password hash
    # JWT token for session management
    jwtToken = Column(String(512), nullable=True)
    # Push token for notifications
    pushToken = Column(String(512), nullable=True)
    isActive = Column(Boolean, default=True)  # Active status of the user
    # Account creation timestamp
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow,
                       onupdate=datetime.utcnow)  # Last update timestamp
    lastLogin = Column(DateTime, nullable=True)  # Last login timestamp
    profileImage = Column(Text, nullable=True)
    address = Column(String(512), nullable=True)
    lat = Column(String(512), nullable=True)
    lng = Column(String(512), nullable=True)
