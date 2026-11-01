"""
Pydantic v2 Schemas for Requests and Responses.
"""

from __future__ import annotations
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


# --- User & Auth Schemas ---
class UserBase(BaseModel):
    username: str
    email: Optional[str] = None
    avatar_url: Optional[str] = None


class UserRead(UserBase):
    id: str
    github_id: int
    created_at: datetime
    plan: str = "free"

    class Config:
        from_attributes = True


class AuthTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserRead


# --- Repository Schemas ---
class RepoCreate(BaseModel):
    github_repo_id: int
    full_name: str
    is_private: bool = False
    default_branch: str = "main"


class RepoRead(BaseModel):
    id: str
    github_repo_id: int
    full_name: str
    is_private: bool
    default_branch: str
    vibe_health_score: int
    last_scanned_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


# --- Scan Schemas ---
class ScanResultRead(BaseModel):
    id: str
    repository_id: str
    commit_sha: Optional[str] = None
    pull_request_number: Optional[int] = None
    score: int
    critical_leaks: int
    high_leaks: int
    conflicts_count: int
    missing_deps_count: int
    details: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime

    class Config:
        from_attributes = True


class OnDemandScanRequest(BaseModel):
    repository_full_name: str
    file_contents: Dict[str, str] = Field(
        default_factory=dict,
        description="Map of relative file paths to string contents for in-memory audit",
    )


# --- Stripe & Billing Schemas ---
class CreateCheckoutSessionRequest(BaseModel):
    plan: str = Field(..., pattern="^(pro|team)$")
    success_url: Optional[str] = None
    cancel_url: Optional[str] = None


class CheckoutSessionResponse(BaseModel):
    checkout_url: str
    session_id: str


class CustomerPortalResponse(BaseModel):
    portal_url: str
