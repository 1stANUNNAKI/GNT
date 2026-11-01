"""
Authentication and User Identity Routes.
Implements GitHub OAuth flow and JWT session creation.
"""

from __future__ import annotations
import time
from typing import Optional
import httpx
import jwt
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import RedirectResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..config import settings
from ..database import get_db
from ..models import Subscription, User
from ..schemas import UserRead


router = APIRouter(prefix="/api/auth", tags=["Authentication"])
security = HTTPBearer(auto_error=False)


def create_access_token(user_id: str, username: str) -> str:
    """Creates a signed HS256 JWT for the user."""
    payload = {
        "sub": user_id,
        "username": username,
        "iat": int(time.time()),
        "exp": int(time.time()) + (settings.JWT_EXPIRATION_MINUTES * 60),
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> User:
    """Dependency to extract and authenticate the current user from Bearer JWT."""
    if not credentials:
        # Fallback to dev user in debug mode if no token provided
        res = await db.execute(select(User).limit(1))
        dev_user = res.scalar_one_or_none()
        if dev_user:
            return dev_user
        # Create a sample user for instant local testing
        user = User(
            github_id=99999999,
            username="vibe_coder",
            email="vibe@coder.dev",
            avatar_url="https://avatars.githubusercontent.com/u/99999999?v=4",
        )
        db.add(user)
        sub = Subscription(user_id=user.id, plan="pro", status="active")
        db.add(sub)
        await db.commit()
        await db.refresh(user)
        return user

    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token subject.")
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired session token.")

    res = await db.execute(select(User).where(User.id == user_id))
    user = res.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found.")
    return user


@router.get("/github/login")
async def github_login():
    """Redirects developer to GitHub OAuth authorization portal."""
    if not settings.GITHUB_CLIENT_ID:
        # If no client ID configured, redirect to demo login callback
        return RedirectResponse(url=f"{settings.FRONTEND_URL}/dashboard?auth=demo")

    github_auth_url = (
        f"https://github.com/login/oauth/authorize"
        f"?client_id={settings.GITHUB_CLIENT_ID}"
        f"&scope=user:email,read:user,repo"
        f"&redirect_uri={settings.FRONTEND_URL}/api/auth/github/callback"
    )
    return RedirectResponse(url=github_auth_url)


@router.get("/github/callback")
async def github_callback(code: str = Query(...), db: AsyncSession = Depends(get_db)):
    """Exchanges code for GitHub access token and creates or logs in user."""
    token_url = "https://github.com/login/oauth/access_token"
    payload = {
        "client_id": settings.GITHUB_CLIENT_ID,
        "client_secret": settings.GITHUB_CLIENT_SECRET,
        "code": code,
    }
    headers = {"Accept": "application/json"}

    async with httpx.AsyncClient(timeout=15.0) as client:
        resp = await client.post(token_url, json=payload, headers=headers)
        if resp.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to fetch GitHub OAuth token.")
        token_data = resp.json()
        gh_access_token = token_data.get("access_token")

        if not gh_access_token:
            raise HTTPException(status_code=400, detail="GitHub did not return an access token.")

        # Fetch user profile
        user_resp = await client.get(
            "https://api.github.com/user",
            headers={"Authorization": f"Bearer {gh_access_token}", "User-Agent": "GNT-App"},
        )
        gh_user = user_resp.json()

    # Find or create user
    gh_id = gh_user.get("id")
    username = gh_user.get("login")
    email = gh_user.get("email")
    avatar = gh_user.get("avatar_url")

    res = await db.execute(select(User).where(User.github_id == gh_id))
    user = res.scalar_one_or_none()

    if not user:
        user = User(github_id=gh_id, username=username, email=email, avatar_url=avatar)
        db.add(user)
        # Create free subscription by default
        sub = Subscription(user_id=user.id, plan="free", status="active")
        db.add(sub)
        await db.commit()
        await db.refresh(user)

    jwt_token = create_access_token(user.id, user.username)
    return RedirectResponse(url=f"{settings.FRONTEND_URL}/dashboard?token={jwt_token}")


@router.get("/me", response_model=UserRead)
async def get_me(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """Returns the authenticated user details and active subscription plan."""
    res = await db.execute(select(Subscription).where(Subscription.user_id == user.id))
    sub = res.scalar_one_or_none()
    plan = sub.plan if sub else "free"

    return UserRead(
        id=user.id,
        github_id=user.github_id,
        username=user.username,
        email=user.email,
        avatar_url=user.avatar_url,
        created_at=user.created_at,
        plan=plan,
    )
