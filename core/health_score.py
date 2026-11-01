"""
Vibe Health Score Engine.
Evaluates repository cleanliness, security posture, and documentation readiness
into a single 0-100 score with visual grading and friendly guidance.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class VibeStatus(str, Enum):
    CERTIFIED = "Vibe Certified 🛡️✨"
    GOOD = "Looking Good 👍"
    NEEDS_ATTENTION = "Needs Attention ⚠️"
    CRITICAL = "Danger Zone 🚨"


@dataclass
class ScorePenalty:
    category: str
    points_deducted: int
    reason: str
    quick_fix: str

    def to_dict(self) -> dict:
        return {
            "category": self.category,
            "points_deducted": self.points_deducted,
            "reason": self.reason,
            "quick_fix": self.quick_fix,
        }


@dataclass
class HealthAuditResult:
    score: int
    status: VibeStatus
    status_color: str  # Hex color code for UI
    penalties: List[ScorePenalty] = field(default_factory=list)
    encouraging_message: str = ""

    def to_dict(self) -> dict:
        return {
            "score": self.score,
            "status": self.status.value,
            "status_color": self.status_color,
            "penalties": [p.to_dict() for p in self.penalties],
            "encouraging_message": self.encouraging_message,
        }


class VibeHealthScore:
    """
    Computes a beginner's repository health index from 0 to 100.
    """

    @classmethod
    def calculate(
        cls,
        critical_secrets_count: int = 0,
        high_secrets_count: int = 0,
        forbidden_files_count: int = 0,
        has_readme: bool = True,
        active_conflicts_count: int = 0,
        missing_dependencies_count: int = 0,
    ) -> HealthAuditResult:
        score = 100
        penalties: List[ScorePenalty] = []

        if critical_secrets_count > 0:
            deduction = min(60, critical_secrets_count * 30)
            score -= deduction
            penalties.append(
                ScorePenalty(
                    category="Security Leak",
                    points_deducted=deduction,
                    reason=f"{critical_secrets_count} live API secret(s) detected in your code!",
                    quick_fix="Revoke those keys on OpenAI/Stripe and move them to an ignored .env file.",
                )
            )

        if forbidden_files_count > 0:
            deduction = min(30, forbidden_files_count * 25)
            score -= deduction
            penalties.append(
                ScorePenalty(
                    category="Tracked Secrets File",
                    points_deducted=deduction,
                    reason="A sensitive file like .env is tracked in git history.",
                    quick_fix="Add .env to .gitignore and untrack it with 'git rm --cached .env'.",
                )
            )

        if high_secrets_count > 0:
            deduction = min(30, high_secrets_count * 15)
            score -= deduction
            penalties.append(
                ScorePenalty(
                    category="High Risk Variable",
                    points_deducted=deduction,
                    reason=f"{high_secrets_count} high-entropy tokens or credentials found.",
                    quick_fix="Extract tokens into environment variables.",
                )
            )

        if not has_readme:
            score -= 15
            penalties.append(
                ScorePenalty(
                    category="Documentation",
                    points_deducted=15,
                    reason="No README.md found in the root directory.",
                    quick_fix="Use the GNT Auto-README generator to create one with one click!",
                )
            )

        if active_conflicts_count > 0:
            deduction = min(40, active_conflicts_count * 20)
            score -= deduction
            penalties.append(
                ScorePenalty(
                    category="Merge Conflicts",
                    points_deducted=deduction,
                    reason=f"{active_conflicts_count} active Git merge conflict marker(s) detected.",
                    quick_fix="Use GNT Conflict Solver to clean merge markers before pushing.",
                )
            )

        if missing_dependencies_count > 0:
            deduction = min(30, missing_dependencies_count * 10)
            score -= deduction
            penalties.append(
                ScorePenalty(
                    category="Missing Dependencies",
                    points_deducted=deduction,
                    reason=f"{missing_dependencies_count} imported library/libraries not saved in requirements.txt or package.json.",
                    quick_fix="Run 'DepDoctor: One-Click Fix' to register them automatically.",
                )
            )

        # Clamp between 0 and 100
        score = max(0, min(100, score))

        if score >= 90:
            status = VibeStatus.CERTIFIED
            color = "#10B981"  # Emerald Green
            msg = "Awesome work! Your repo is safe, clean, and beginner-proof. Ready to deploy! 🚀"
        elif score >= 70:
            status = VibeStatus.GOOD
            color = "#8B5CF6"  # Electric Violet
            msg = "Looking great! Just a couple of minor items to polish before your big release."
        elif score >= 50:
            status = VibeStatus.NEEDS_ATTENTION
            color = "#F59E0B"  # Amber
            msg = "Almost there! Take a look at the quick fixes above to protect your app from build or security bugs."
        else:
            status = VibeStatus.CRITICAL
            color = "#EF4444"  # Crimson Red
            msg = "Action needed! Leaked keys or broken files detected. Don't worry—follow the one-click fixes above!"

        return HealthAuditResult(
            score=score,
            status=status,
            status_color=color,
            penalties=penalties,
            encouraging_message=msg,
        )
