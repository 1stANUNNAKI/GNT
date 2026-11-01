"""
GitHub App FastAPI Webhook Server.
Entrypoint for processing GitHub webhooks and running safety automation.
"""

from __future__ import annotations
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Header, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from .webhook_handler import GitHubWebhookHandler


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup setup
    print("[GNT] GitHub App Server started listening for webhooks.")
    yield
    print("[GNT] GitHub App Server shutting down.")


app = FastAPI(
    title="GitHub Noob Toolkit (GNT) - App Webhook Server",
    description="Automated safety, leak shield, and vibe copilot for GitHub repositories.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

webhook_handler = GitHubWebhookHandler()


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "gnt-github-app",
        "version": "1.0.0",
    }


@app.post("/api/github/webhook")
async def receive_github_webhook(
    request: Request,
    x_github_event: str = Header(..., alias="X-GitHub-Event"),
    x_hub_signature_256: str = Header(None, alias="X-Hub-Signature-256"),
):
    """
    Receives and processes GitHub webhook events with HMAC signature verification.
    """
    body_bytes = await request.body()

    # If secret is set in environment, enforce strict HMAC verification
    webhook_secret = os.getenv("GITHUB_WEBHOOK_SECRET")
    if webhook_secret:
        if not webhook_handler.verify_signature(body_bytes, x_hub_signature_256):
            raise HTTPException(status_code=401, detail="Invalid HMAC webhook signature.")

    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON payload.")

    result = await webhook_handler.handle_event(event_type=x_github_event, payload=payload)
    return {"ok": True, "result": result}
