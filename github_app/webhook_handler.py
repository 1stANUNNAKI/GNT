"""
GitHub App Webhook Handler Module.
Verifies HMAC SHA-256 signatures, coordinates security scans,
triggers GitHub Checks API updates, and posts friendly reviews.
"""

from __future__ import annotations
import hashlib
import hmac
import json
import os
from typing import Any, Dict, List, Optional, Tuple
import httpx

from core.secrets import SecretShield, SecretFinding, Severity
from core.vibelog import VibeLog, ChangelogSummary
from core.conflicts import ConflictSolver, ConflictResolution
from .auth import GitHubAppAuth
from .checks_api import ChecksApiClient, CheckAnnotation
from .pr_commenter import PRCommenter


class GitHubWebhookHandler:
    """
    Main webhook coordinator for the GitHub App.
    """

    def __init__(self, webhook_secret: Optional[str] = None, auth: Optional[GitHubAppAuth] = None):
        self.webhook_secret = (webhook_secret or os.getenv("GITHUB_WEBHOOK_SECRET", "")).encode("utf-8")
        self.auth = auth or GitHubAppAuth()
        self.secret_shield = SecretShield()

    def verify_signature(self, payload_bytes: bytes, signature_header: Optional[str]) -> bool:
        """
        Verifies that the payload was sent by GitHub using HMAC SHA-256.
        """
        if not signature_header or not signature_header.startswith("sha256="):
            return False
        expected_hash = signature_header[7:]

        mac = hmac.new(self.webhook_secret, msg=payload_bytes, digestmod=hashlib.sha256)
        return hmac.compare_digest(mac.hexdigest(), expected_hash)

    async def handle_event(self, event_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Dispatches incoming GitHub webhook events to specialized handlers.
        """
        if event_type == "pull_request":
            action = payload.get("action")
            if action in ("opened", "synchronize", "reopened"):
                return await self.handle_pull_request(payload)
            return {"status": "ignored", "reason": f"Unhandled pull_request action: {action}"}

        elif event_type == "push":
            return await self.handle_push(payload)

        return {"status": "ignored", "reason": f"Unhandled event type: {event_type}"}

    async def handle_pull_request(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processes pull requests: fetches diff, executes scans, updates Checks API, and posts comments.
        """
        installation_id = payload.get("installation", {}).get("id")
        repository = payload.get("repository", {})
        owner = repository.get("owner", {}).get("login")
        repo = repository.get("name")
        pr_data = payload.get("pull_request", {})
        pull_number = pr_data.get("number")
        head_sha = pr_data.get("head", {}).get("sha")
        diff_url = pr_data.get("diff_url")

        if not all([owner, repo, head_sha]):
            return {"status": "error", "message": "Missing repository or pull request details"}

        # Obtain scoped installation token if configured
        token = ""
        if installation_id:
            try:
                token = await self.auth.get_installation_access_token(installation_id)
            except Exception as e:
                # Log error and continue with dry run or limited permissions
                token = os.getenv("GITHUB_TOKEN", "")
        else:
            token = os.getenv("GITHUB_TOKEN", "")

        # 1. Fetch unified diff
        diff_text = await self._fetch_diff(diff_url, token)

        # 2. Run GNT Core Inspection Engines
        secret_findings = self.secret_shield.scan_git_diff(diff_text)
        changelog = VibeLog.parse_diff(diff_text, commit_message=pr_data.get("title"))
        conflict_analysis = ConflictSolver.analyze_file_content(diff_text)

        # 3. If token is present, update Checks API & post comment
        if token:
            checks_client = ChecksApiClient(installation_token=token)
            try:
                check_id = await checks_client.create_check_run(owner=owner, repo=repo, head_sha=head_sha)
                
                # Formulate annotations for any detected leaks
                annotations: List[CheckAnnotation] = []
                has_critical_leaks = False

                for finding in secret_findings:
                    level = "failure" if finding.severity == Severity.CRITICAL else "warning"
                    if finding.severity == Severity.CRITICAL:
                        has_critical_leaks = True

                    annotations.append(
                        CheckAnnotation(
                            path=finding.file_path,
                            start_line=finding.line_number,
                            end_line=finding.line_number,
                            annotation_level=level,
                            title=finding.rule_name,
                            message=f"{finding.friendly_explanation}\nQuick fix: {finding.remediation_steps[0]}",
                        )
                    )

                conclusion = "failure" if (has_critical_leaks or conflict_analysis.has_conflicts) else "success"
                title = (
                    "🚨 GNT Shield: Action Required!"
                    if conclusion == "failure"
                    else "✨ GNT Shield: All Clear! 100% Vibe Passed"
                )
                summary_text = (
                    f"Scanned {len(secret_findings)} secret alert(s). "
                    f"Vibe Health Score updated. Review comments below for instant one-click fixes."
                )

                await checks_client.complete_check_run(
                    owner=owner,
                    repo=repo,
                    check_run_id=check_id,
                    conclusion=conclusion,
                    title=title,
                    summary=summary_text,
                    annotations=annotations,
                )
            except Exception as e:
                pass  # Do not crash webhook if GitHub Check API call fails

            # Post comment to PR
            commenter = PRCommenter(installation_token=token)
            try:
                await commenter.post_or_update_pr_comment(
                    owner=owner,
                    repo=repo,
                    pull_number=pull_number,
                    secrets=secret_findings,
                    changelog=changelog,
                    conflict_res=conflict_analysis,
                )
            except Exception:
                pass

        return {
            "status": "processed",
            "pull_request": pull_number,
            "secrets_found": len(secret_findings),
            "conflicts_found": conflict_analysis.total_conflicts,
            "vibe_headline": changelog.vibe_headline,
        }

    async def handle_push(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Handles branch push events."""
        commits = payload.get("commits", [])
        return {"status": "processed", "commits_evaluated": len(commits)}

    async def _fetch_diff(self, diff_url: Optional[str], token: str) -> str:
        """Downloads the raw git diff from GitHub."""
        if not diff_url:
            return ""
        headers = {
            "Accept": "application/vnd.github.v3.diff",
            "User-Agent": "GitHub-Noob-Toolkit/1.0",
        }
        if token:
            headers["Authorization"] = f"token {token}"

        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                resp = await client.get(diff_url, headers=headers)
                if resp.status_code == 200:
                    return resp.text
        except Exception:
            pass
        return ""
