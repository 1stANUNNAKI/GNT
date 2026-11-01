"""
Backend Configuration Module.
Loads environment variables using Pydantic Settings.
"""

from __future__ import annotations
import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "GitHub Noob Toolkit (GNT)"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    PORT: int = 8000

    # Frontend URL for redirects & CORS
    FRONTEND_URL: str = "http://localhost:3000"

    # Database: Supports PostgreSQL asyncpg or SQLite fallback
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./gnt.db")

    # JWT Authentication
    JWT_SECRET: str = "gnt_super_secret_jwt_encryption_key_change_in_production_32b"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 60 * 24 * 7  # 7 days

    # GitHub OAuth & App Config
    GITHUB_CLIENT_ID: str = ""
    GITHUB_CLIENT_SECRET: str = ""
    GITHUB_APP_ID: str = ""
    GITHUB_PRIVATE_KEY: str = ""
    GITHUB_WEBHOOK_SECRET: str = ""

    # Stripe Billing
    STRIPE_SECRET_KEY: str = ""
    STRIPE_PUBLISHABLE_KEY: str = ""
    STRIPE_WEBHOOK_SECRET: str = ""
    STRIPE_PRICE_ID_PRO: str = "price_pro_monthly"
    STRIPE_PRICE_ID_TEAM: str = "price_team_monthly"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
