"""
GitHub Checks API Integration Module.
Creates and updates check runs with rich annotations and friendly advice.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import httpx


@dataclass
class CheckAnnotation:
    path: str
    start_line: int
    end_line: int
    annotation_level: str  # "failure", "warning", "notice"
    title: str
    message: str
    raw_details: Optional[str] = None

    def to_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "path": self.path,
            "start_line": self.start_line,
            "end_line": self.end_line,
            "annotation_level": self.annotation_level,
            "title": self.title,
            "message": self.message,
        }
        if self.raw_details:
            payload["raw_details"] = self.raw_details
        return payload


class ChecksApiClient:
    """
    Communicates with GitHub Checks API to block unsafe PRs or display helpful hints.
    """

    def __init__(self, installation_token: str):
        self.headers = {
            "Authorization": f"token {installation_token}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "GitHub-Noob-Toolkit/1.0",
        }

    async def create_check_run(
        self,
        owner: str,
        repo: str,
        head_sha: str,
        name: str = "GNT / Safety & Vibe Shield",
    ) -> int:
        """
        Initializes a Check Run in the 'in_progress' state.
        """
        url = f"https://api.github.com/repos/{owner}/{repo}/check-runs"
        payload = {
            "name": name,
            "head_sha": head_sha,
            "status": "in_progress",
            "output": {
                "title": "Shielding your code...",
                "summary": "GitHub Noob Toolkit is scanning your diff for leaked secrets, conflicts, and missing packages.",
            },
        }

        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.post(url, headers=self.headers, json=payload)
            if resp.status_code not in (200, 201):
                raise RuntimeError(f"Failed to create check run: {resp.status_code} {resp.text}")
            return resp.json()["id"]

    async def complete_check_run(
        self,
        owner: str,
        repo: str,
        check_run_id: int,
        conclusion: str,  # "success", "failure", "neutral"
        title: str,
        summary: str,
        annotations: Optional[List[CheckAnnotation]] = None,
    ) -> Dict[str, Any]:
        """
        Completes the check run with a conclusion and up to 50 annotations per request.
        """
        url = f"https://api.github.com/repos/{owner}/{repo}/check-runs/{check_run_id}"
        formatted_annotations = [a.to_payload() for a in (annotations or [])[:50]]

        payload: Dict[str, Any] = {
            "status": "completed",
            "conclusion": conclusion,
            "output": {
                "title": title,
                "summary": summary,
                "annotations": formatted_annotations,
            },
        }

        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.patch(url, headers=self.headers, json=payload)
            if resp.status_code not in (200, 201):
                raise RuntimeError(f"Failed to update check run: {resp.status_code} {resp.text}")
            return resp.json()
