"""
Human Changelog Module (VibeLog).
Translates intimidating Git diffs and pull requests into friendly, jargon-free
changelogs with emojis, empathy, and clear categories.
"""

from __future__ import annotations
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class ChangelogSummary:
    features: List[str] = field(default_factory=list)
    fixes: List[str] = field(default_factory=list)
    breaking_changes: List[str] = field(default_factory=list)
    chores: List[str] = field(default_factory=list)
    total_files_changed: int = 0
    total_lines_added: int = 0
    total_lines_removed: int = 0
    vibe_headline: str = ""
    no_jargon_summary: str = ""

    def to_markdown(self) -> str:
        lines = [f"## 📝 What changed? ({self.vibe_headline})", ""]
        lines.append(f"> **Quick Summary:** {self.no_jargon_summary}")
        lines.append("")

        if self.features:
            lines.append("### ✨ New Features & Upgrades")
            for item in self.features:
                lines.append(f"- {item}")
            lines.append("")

        if self.fixes:
            lines.append("### 🐛 Fixes & Polishing")
            for item in self.fixes:
                lines.append(f"- {item}")
            lines.append("")

        if self.breaking_changes:
            lines.append("### ⚠️ Heads Up! (Things to Double Check)")
            for item in self.breaking_changes:
                lines.append(f"- {item}")
            lines.append("")

        if self.chores:
            lines.append("### 🧹 Behind the Scenes (Maintenance)")
            for item in self.chores:
                lines.append(f"- {item}")
            lines.append("")

        lines.append(
            f"📊 *Stats: {self.total_files_changed} files touched, +{self.total_lines_added} lines added, -{self.total_lines_removed} lines removed.*"
        )
        return "\n".join(lines)


class VibeLog:
    """
    Parses unified diffs, commit messages, and modified syntax to synthesize
    human-readable progress reports.
    """

    FEATURE_KEYWORDS = ["add", "feat", "create", "new", "implement", "support", "button", "screen", "endpoint", "page"]
    FIX_KEYWORDS = ["fix", "bug", "patch", "resolve", "correct", "prevent", "crash", "error", "typo", "leak"]
    BREAKING_KEYWORDS = ["breaking", "deprecate", "remove", "drop", "delete table", "drop column", "migrate", "rename api"]
    CHORE_KEYWORDS = ["clean", "refactor", "chore", "bump", "update", "format", "style", "test", "lint", "docs"]

    @classmethod
    def parse_diff(cls, diff_text: str, commit_message: Optional[str] = None) -> ChangelogSummary:
        """
        Parses a git diff and produces an empathetic, human-friendly summary.
        """
        summary = ChangelogSummary()
        files_modified: set[str] = set()
        added_lines: List[str] = []
        removed_lines: List[str] = []

        file_diff_pattern = re.compile(r"^\+\+\+\s+b/(.*)$")

        for line in diff_text.splitlines():
            fmatch = file_diff_pattern.match(line)
            if fmatch:
                files_modified.add(fmatch.group(1).strip())
                continue

            if line.startswith("+") and not line.startswith("+++"):
                summary.total_lines_added += 1
                clean = line[1:].strip()
                if len(clean) > 5 and not clean.startswith("//") and not clean.startswith("#"):
                    added_lines.append(clean)
            elif line.startswith("-") and not line.startswith("---"):
                summary.total_lines_removed += 1
                clean = line[1:].strip()
                if len(clean) > 5:
                    removed_lines.append(clean)

        summary.total_files_changed = len(files_modified)

        # 1. Synthesize Features
        for filename in files_modified:
            lower_name = filename.lower()
            if "route" in lower_name or "api" in lower_name:
                summary.features.append(f"Added or expanded backend endpoint in `{filename}`")
            elif "page" in lower_name or "view" in lower_name or "component" in lower_name:
                summary.features.append(f"Built or updated user interface component in `{filename}`")
            elif "model" in lower_name or "schema" in lower_name:
                summary.features.append(f"Defined new data structure or database schema in `{filename}`")

        # 2. Extract specific clues from added code lines
        for line in added_lines[:50]:
            lower = line.lower()
            if any(k in lower for k in ["stripe", "payment", "checkout"]):
                item = "Integrated payment checkout functionality"
                if item not in summary.features:
                    summary.features.append(item)
            elif any(k in lower for k in ["try:", "catch", "except", "error handling"]):
                item = "Added safety shields to catch unexpected runtime crashes gracefully"
                if item not in summary.fixes:
                    summary.fixes.append(item)
            elif any(k in lower for k in ["validate", "sanitiz", "regex"]):
                item = "Strengthened form validation and input security"
                if item not in summary.fixes:
                    summary.fixes.append(item)

        # 3. Detect Breaking changes (removed critical endpoints or functions)
        for line in removed_lines[:50]:
            lower = line.lower()
            if any(k in lower for k in ["def ", "function ", "export const ", "class "]):
                # If deleted without being just a rename
                if any(b in lower for b in ["api", "auth", "user", "token"]):
                    summary.breaking_changes.append(f"Removed or refactored core declaration: `{line[:60]}...`")

        # 4. Maintenance / Chores
        for filename in files_modified:
            lower = filename.lower()
            if lower.endswith((".json", ".toml", ".txt")) and ("package" in lower or "requirement" in lower):
                summary.chores.append(f"Updated library packages & dependency manifests in `{filename}`")
            elif "docker" in lower or "compose" in lower:
                summary.chores.append(f"Optimized container build & deployment configuration in `{filename}`")
            elif "test" in lower:
                summary.chores.append(f"Expanded test automation suite in `{filename}`")

        # Fallback if no specific feature was matched
        if not summary.features and summary.total_lines_added > 0:
            summary.features.append(f"Added code enhancements across {len(files_modified)} files")

        if commit_message:
            msg_lower = commit_message.lower()
            if any(k in msg_lower for k in cls.FIX_KEYWORDS) and not summary.fixes:
                summary.fixes.append(f"Applied fix: {commit_message}")

        # Set human headline & non-jargon explanation
        if summary.breaking_changes:
            summary.vibe_headline = "Big structural improvements (Take a peek at breaking changes!)"
            summary.no_jargon_summary = (
                "You modified some key functions that other parts of your app might depend on. "
                "Make sure to test your main user flows to ensure everything connects smoothly!"
            )
        elif summary.features and summary.fixes:
            summary.vibe_headline = "New power-ups and bug squashing! 🎉"
            summary.no_jargon_summary = (
                "Great job! You added new functionality to your project while also fixing issues. "
                "The codebase is cleaner and more capable now."
            )
        elif summary.fixes:
            summary.vibe_headline = "Smooth bug fixes & reliability boost 🛡️"
            summary.no_jargon_summary = (
                "This update focuses on making the app more stable. Things should run smoother without hiccups."
            )
        else:
            summary.vibe_headline = "Fresh updates & progress 🚀"
            summary.no_jargon_summary = (
                "New code was committed to move your app forward. Everything is looking clean and ready to test."
            )

        return summary
