"""
GitHub App Authentication Module.
Generates RSA Private Key RS256 JWTs and exchanges them for Installation Access Tokens.
"""

from __future__ import annotations
import os
import time
from typing import Optional
import httpx
import jwt


class GitHubAppAuth:
    """
    Handles cryptographic RS256 signing and ephemeral installation tokens for GitHub Apps.
    """

    def __init__(
        self,
        app_id: Optional[str] = None,
        private_key_pem: Optional[str] = None,
        private_key_path: Optional[str] = None,
    ):
        self.app_id = app_id or os.getenv("GITHUB_APP_ID", "")
        self.private_key_pem = private_key_pem or os.getenv("GITHUB_PRIVATE_KEY", "")

        if not self.private_key_pem and private_key_path and os.path.exists(private_key_path):
            with open(private_key_path, "r", encoding="utf-8") as f:
                self.private_key_pem = f.read()

        # Clean escaped newlines if passed through environment strings
        if self.private_key_pem and "\\n" in self.private_key_pem:
            self.private_key_pem = self.private_key_pem.replace("\\n", "\n")

    def generate_app_jwt(self, expiration_seconds: int = 540) -> str:
        """
        Generates an RS256 signed JWT valid for up to 10 minutes to authenticate as the GitHub App.
        """
        if not self.app_id:
            raise ValueError("GITHUB_APP_ID is not configured.")
        if not self.private_key_pem:
            raise ValueError("GITHUB_PRIVATE_KEY is not configured.")

        now = int(time.time())
        payload = {
            "iat": now - 60,  # 60s in the past to prevent clock drift issues
            "exp": now + expiration_seconds,
            "iss": str(self.app_id),
        }

        token = jwt.encode(payload, self.private_key_pem, algorithm="RS256")
        return token

    async def get_installation_access_token(self, installation_id: int) -> str:
        """
        Exchanges the App JWT for a scoped Installation Access Token via GitHub REST API.
        """
        app_jwt = self.generate_app_jwt()
        headers = {
            "Authorization": f"Bearer {app_jwt}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "GitHub-Noob-Toolkit/1.0",
        }

        url = f"https://api.github.com/app/installations/{installation_id}/access_tokens"
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.post(url, headers=headers)
            if resp.status_code != 201:
                raise RuntimeError(
                    f"Failed to obtain installation token for ID {installation_id}: {resp.status_code} {resp.text}"
                )
            data = resp.json()
            return data["token"]
