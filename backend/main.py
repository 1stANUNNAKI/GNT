"""
FastAPI Main Application for GitHub Noob Toolkit (GNT) SaaS Platform.
Unified REST API serving Authentication, Repositories, Scans, Billing, and Webhooks.
"""

from __future__ import annotations
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .database import init_db
from .routes.auth import router as auth_router
from .routes.repos import router as repos_router
from .routes.scans import router as scans_router
from .routes.billing import router as billing_router
from github_app.main import app as github_app_subapp


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database schemas
    await init_db()
    print("[GNT] Database initialized & ready.")
    yield
    print("[GNT] SaaS Backend shutdown cleanly.")


app = FastAPI(
    title="GitHub Noob Toolkit (GNT) - SaaS API",
    description="Protective shield & automation copilot for beginners and vibe coders.",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware for Next.js frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:3001", "http://127.0.0.1:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount REST API Routers
app.include_router(auth_router)
app.include_router(repos_router)
app.include_router(scans_router)
app.include_router(billing_router)

# Mount GitHub App webhook server under /github-app or alongside
app.mount("/github-app", github_app_subapp)


@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "gnt-saas-api",
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=settings.PORT, reload=settings.DEBUG)
