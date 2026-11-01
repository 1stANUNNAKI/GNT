"""
GitHub Noob Toolkit (GNT) - Core Safety and Repair Engine.
Tailored for beginners, non-traditional developers, and vibe coders.
"""

from .secrets import SecretShield, SecretFinding
from .docgen import DocGen, ProjectAnalysis
from .vibelog import VibeLog, ChangelogSummary
from .conflicts import ConflictSolver, ConflictResolution
from .dependencies import DepDoctor, MissingDependencyFinding
from .health_score import VibeHealthScore, HealthAuditResult

__all__ = [
    "SecretShield",
    "SecretFinding",
    "DocGen",
    "ProjectAnalysis",
    "VibeLog",
    "ChangelogSummary",
    "ConflictSolver",
    "ConflictResolution",
    "DepDoctor",
    "MissingDependencyFinding",
    "VibeHealthScore",
    "HealthAuditResult",
]
