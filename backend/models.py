"""
SQLAlchemy 2.0 Database Models for GNT SaaS Platform.
"""

from __future__ import annotations
import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base


def generate_uuid() -> str:
    return str(uuid.uuid4())


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    github_id: Mapped[int] = mapped_column(Integer, unique=True, index=True)
    username: Mapped[str] = mapped_column(String(100), index=True)
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    avatar_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    subscription: Mapped[Optional["Subscription"]] = relationship(back_populates="user", uselist=False, cascade="all, delete-orphan")
    repositories: Mapped[List["Repository"]] = relationship(back_populates="user", cascade="all, delete-orphan")


class Subscription(Base):
    __tablename__ = "subscriptions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    stripe_customer_id: Mapped[Optional[str]] = mapped_column(String(100), unique=True, nullable=True)
    stripe_subscription_id: Mapped[Optional[str]] = mapped_column(String(100), unique=True, nullable=True)
    plan: Mapped[str] = mapped_column(String(50), default="free")  # "free", "pro", "team"
    status: Mapped[str] = mapped_column(String(50), default="active")  # "active", "canceled", "past_due"
    current_period_end: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="subscription")


class Repository(Base):
    __tablename__ = "repositories"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"))
    github_repo_id: Mapped[int] = mapped_column(Integer, index=True)
    full_name: Mapped[str] = mapped_column(String(200), index=True)  # e.g., "username/project"
    is_private: Mapped[bool] = mapped_column(Boolean, default=False)
    default_branch: Mapped[str] = mapped_column(String(100), default="main")
    vibe_health_score: Mapped[int] = mapped_column(Integer, default=100)
    last_scanned_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="repositories")
    scans: Mapped[List["ScanResult"]] = relationship(back_populates="repository", cascade="all, delete-orphan")


class ScanResult(Base):
    __tablename__ = "scan_results"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    repository_id: Mapped[str] = mapped_column(String(36), ForeignKey("repositories.id", ondelete="CASCADE"))
    commit_sha: Mapped[Optional[str]] = mapped_column(String(40), nullable=True)
    pull_request_number: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    score: Mapped[int] = mapped_column(Integer, default=100)
    critical_leaks: Mapped[int] = mapped_column(Integer, default=0)
    high_leaks: Mapped[int] = mapped_column(Integer, default=0)
    conflicts_count: Mapped[int] = mapped_column(Integer, default=0)
    missing_deps_count: Mapped[int] = mapped_column(Integer, default=0)
    details_json: Mapped[str] = mapped_column(Text, default="{}")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    repository: Mapped["Repository"] = relationship(back_populates="scans")
