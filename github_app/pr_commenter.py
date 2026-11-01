"""
Empathetic PR Commenter Module.
Leaves helpful, non-shaming comments on pull requests with clear guidance and changelogs.
"""

from __future__ import annotations
from typing import Any, Dict, List, Optional
import httpx
from core.vibelog import ChangelogSummary
from core.secrets import SecretFinding
from core.conflicts import ConflictResolution


class PRCommenter:
    """
    Communicates with developers on GitHub Pull Requests in a supportive, beginner-friendly tone.
    """

    def __init__(self, installation_token: str):
        self.headers = {
            "Authorization": f"token {installation_token}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "GitHub-Noob-Toolkit/1.0",
        }

    async def post_or_update_pr_comment(
        self,
        owner: str,
        repo: str,
        pull_number: int,
        secrets: List[SecretFinding],
        changelog: ChangelogSummary,
        conflict_res: Optional[ConflictResolution] = None,
    ) -> Dict[str, Any]:
        """
        Formats and publishes the GNT Copilot review message.
        """
        url = f"https://api.github.com/repos/{owner}/{repo}/issues/{pull_number}/comments"
        body = self._format_comment_markdown(secrets, changelog, conflict_res)

        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.post(url, headers=self.headers, json={"body": body})
            if resp.status_code not in (200, 201):
                raise RuntimeError(f"Failed to post comment to PR #{pull_number}: {resp.status_code} {resp.text}")
            return resp.json()

    def _format_comment_markdown(
        self,
        secrets: List[SecretFinding],
        changelog: ChangelogSummary,
        conflict_res: Optional[ConflictResolution] = None,
    ) -> str:
        blocks = [
            "<!-- GNT-BOT-COMMENT -->",
            "## 🛡️ GitHub Noob Toolkit (GNT) · Copilot Review",
            "",
        ]

        if secrets:
            blocks.append("### 🚨 Safety Shield Triggered!")
            blocks.append(
                "> **Don't panic!** We caught sensitive keys before they got merged into your codebase. "
                "Everyone makes this mistake when starting out. Here is what we found:"
            )
            blocks.append("")
            for s in secrets:
                blocks.append(f"- **{s.rule_name}** in `{s.file_path}` (Line {s.line_number})")
                blocks.append(f"  - *What happened:* {s.friendly_explanation}")
                blocks.append(f"  - *Quick Fix:* `{s.remediation_steps[0]}`")
            blocks.append("")
            blocks.append("💡 *Tip: Move these secrets to your local `.env` file, commit the change, and push again.*")
            blocks.append("")

        if conflict_res and conflict_res.has_conflicts:
            blocks.append("### ⚔️ Branch Conflict Detected")
            blocks.append(f"> {conflict_res.summary_message}")
            blocks.append("")

        # Always include friendly changelog
        blocks.append("---")
        blocks.append(changelog.to_markdown())
        blocks.append("")
        blocks.append("---")
        blocks.append(
            "*Powered by [GitHub Noob Toolkit](https://github.com/gnt-shield) — Protecting vibe coders everywhere.*"
        )

        return "\n".join(blocks)
