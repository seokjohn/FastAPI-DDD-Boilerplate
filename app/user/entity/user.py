from uuid import uuid4
from datetime import timedelta, datetime
from sqlalchemy import (
    func,
    Column,
    Boolean,
    String,
    Enum,
    LargeBinary,
    DateTime,
    ForeignKey,
    Integer
)
from sqlalchemy.orm import relationship

from core.db import Base
from app.user.enums.user import UserStatus

class Users(Base):
    __tablename__ = "users"
    id = Column(String(length=36), primary_key=True, default=lambda: str(uuid4()))
    email = Column(String(length=50), nullable=True, unique=True)
    status = Column(Enum(UserStatus), default=UserStatus.active)
    is_staff = Column(Boolean, nullable=True, default=False)
    is_superuser = Column(Boolean, nullable=True, default=False)
    deleted_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=func.current_timestamp())
    updated_at = Column(DateTime, nullable=False, default=func.current_timestamp(), onupdate=func.current_timestamp())

    profile = relationship("Profiles", lazy='joined', uselist=False, backref="users")

class Profiles(Base):
    __tablename__ = "profiles"
    id = Column(String(length=36), primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String(length=36), ForeignKey('users.id', ondelete='CASCADE'), index=True)
    nick_name = Column(String(length=50), nullable=True, index=True)
    picture_url = Column(String(length=255), nullable=True)

    deleted_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=func.current_timestamp())
    updated_at = Column(DateTime, nullable=False, default=func.current_timestamp(), onupdate=func.current_timestamp())