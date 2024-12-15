from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from app.database.base import Base
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(512), nullable=True)  # Full name of the user
    email = Column(String(512), unique=True, nullable=True)  # Email ID
    # Optional phone number
    phone = Column(String(512), unique=True, nullable=False)
    password_hash = Column(String(512), nullable=True)  # Password hash
    # JWT token for session management
    jwt_token = Column(String(512), nullable=True)
    # Push token for notifications
    push_token = Column(String(512), nullable=True)
    is_active = Column(Boolean, default=True)  # Active status of the user
    # Account creation timestamp
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)  # Last update timestamp
    last_login = Column(DateTime, nullable=True)  # Last login timestamp
    profileImage = Column(String(512), nullable=True)
    