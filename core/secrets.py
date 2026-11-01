"""
Secret Leak Shield Module.
Scans diffs, source files, and commit payloads using regex signatures,
Shannon entropy evaluation, and .gitignore auditing.
"""

from __future__ import annotations
import math
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Tuple


class Severity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class SecretFinding:
    rule_id: str
    rule_name: str
    severity: Severity
    file_path: str
    line_number: int
    raw_match: str
    masked_value: str
    friendly_explanation: str
    remediation_steps: List[str]
    entropy: float = 0.0

    def to_dict(self) -> dict:
        return {
            "rule_id": self.rule_id,
            "rule_name": self.rule_name,
            "severity": self.severity.value,
            "file_path": self.file_path,
            "line_number": self.line_number,
            "masked_value": self.masked_value,
            "friendly_explanation": self.friendly_explanation,
            "remediation_steps": self.remediation_steps,
            "entropy": round(self.entropy, 2),
        }


class SecretShield:
    """
    Detects exposed secrets in code, git diffs, and tracked file trees.
    Includes Shannon entropy estimation and friendly, non-shaming remediation tips.
    """

    # Signatures for known secret formats
    KNOWN_PATTERNS: List[Tuple[str, str, Severity, re.Pattern, str]] = [
        (
            "OPENAI_KEY",
            "OpenAI API Key",
            Severity.CRITICAL,
            re.compile(r"(sk-(?:proj-)?[A-Za-z0-9_\-]{32,80})"),
            "This is your OpenAI secret key! If someone gets this, they can use your account to run costly AI models.",
        ),
        (
            "STRIPE_SECRET_KEY",
            "Stripe Secret Key",
            Severity.CRITICAL,
            re.compile(r"((?:sk|rk)_(?:live|test)_[0-9a-zA-Z]{24,60})"),
            "This is a Stripe secret payment key! Exposing live keys allows anyone to issue charges or refunds.",
        ),
        (
            "AWS_ACCESS_KEY_ID",
            "AWS Access Key ID",
            Severity.HIGH,
            re.compile(r"(AKIA[0-9A-Z]{16})"),
            "This is an AWS Access Key. Cloud crawlers scan GitHub 24/7 to hijack cloud infrastructure with these.",
        ),
        (
            "AWS_SECRET_ACCESS_KEY",
            "AWS Secret Access Key",
            Severity.CRITICAL,
            re.compile(r"(?i)aws_secret_access_key\s*[:=]\s*['\"]([A-Za-z0-9/+=]{40})['\"]"),
            "This is an AWS Secret Access Key paired with an AWS ID to access your entire cloud console.",
        ),
        (
            "GITHUB_PAT",
            "GitHub Personal Access Token",
            Severity.CRITICAL,
            re.compile(r"(ghp_[0-9a-zA-Z]{36}|github_pat_[0-9a-zA-Z_]{82})"),
            "This is your personal GitHub account token. Anyone possessing it can modify your private repos.",
        ),
        (
            "ANTHROPIC_KEY",
            "Anthropic Claude API Key",
            Severity.CRITICAL,
            re.compile(r"(sk-ant-[0-9a-zA-Z_\-]{32,80})"),
            "This is an Anthropic Claude API key. Keep it in your .env file so others cannot spend your credits.",
        ),
        (
            "GOOGLE_AI_KEY",
            "Google AI / Gemini API Key",
            Severity.HIGH,
            re.compile(r"(AIzaSy[0-9A-Za-z_\-]{33})"),
            "This is a Google Cloud / Gemini API key. Restrict it in Google Cloud Console immediately.",
        ),
        (
            "SLACK_TOKEN",
            "Slack Bot / User Token",
            Severity.HIGH,
            re.compile(r"(xox[baprs]-[0-9a-zA-Z]{10,48})"),
            "This is a Slack token that allows reading or posting messages to your team workspace.",
        ),
        (
            "PRIVATE_KEY_BLOCK",
            "Cryptographic Private Key",
            Severity.CRITICAL,
            re.compile(r"(-----BEGIN (?:[A-Z0-9 ]+ )?PRIVATE KEY-----)"),
            "This is a raw cryptographic private key (SSH / SSL / RSA). Never commit this file to version control!",
        ),
        (
            "DATABASE_URI_WITH_AUTH",
            "Database Connection URI with Password",
            Severity.HIGH,
            re.compile(r"((?:postgres|postgresql|mysql|mongodb|redis)://[^:]+:([^@]+)@[a-zA-Z0-9._\-]+)"),
            "Your database connection string contains a raw password. Store database URLs in environment variables.",
        ),
    ]

    # Sensitive filenames that should NEVER be tracked in Git
    FORBIDDEN_FILES = [
        (".env", Severity.CRITICAL, "Environment file containing live credentials"),
        (".env.local", Severity.CRITICAL, "Local environment file containing private keys"),
        (".env.production", Severity.CRITICAL, "Production environment secrets"),
        ("id_rsa", Severity.CRITICAL, "SSH private key file"),
        ("id_ed25519", Severity.CRITICAL, "SSH private key file"),
        ("credentials.json", Severity.HIGH, "Service account or OAuth credentials file"),
        ("serviceAccountKey.json", Severity.HIGH, "Google Cloud or Firebase service account key"),
        (".npmrc", Severity.MEDIUM, "May contain NPM authentication tokens"),
    ]

    @staticmethod
    def calculate_shannon_entropy(data: str) -> float:
        """Calculates the Shannon entropy (randomness) of a string."""
        if not data:
            return 0.0
        entropy = 0.0
        length = len(data)
        frequencies = {char: data.count(char) for char in set(data)}
        for count in frequencies.values():
            probability = count / length
            entropy -= probability * math.log2(probability)
        return entropy

    @staticmethod
    def mask_secret(secret: str) -> str:
        """Safely masks a secret string, leaving only tiny hint characters."""
        if len(secret) <= 8:
            return "*" * len(secret)
        prefix_len = min(4, len(secret) // 4)
        suffix_len = min(4, len(secret) // 4)
        hidden_len = len(secret) - prefix_len - suffix_len
        return f"{secret[:prefix_len]}{'*' * hidden_len}{secret[-suffix_len:]}"

    def audit_file_path(self, file_path: str) -> Optional[SecretFinding]:
        """Checks if a file being added or committed is a forbidden sensitive file."""
        normalized = file_path.replace("\\", "/").strip().lower()
        file_name = normalized.split("/")[-1]

        for forbidden, severity, reason in self.FORBIDDEN_FILES:
            if file_name == forbidden.lower() or file_name.endswith(f".{forbidden.lower()}"):
                return SecretFinding(
                    rule_id="FORBIDDEN_FILE_TRACKED",
                    rule_name=f"Forbidden File: {forbidden}",
                    severity=severity,
                    file_path=file_path,
                    line_number=1,
                    raw_match=file_path,
                    masked_value="[RESTRICTED FILENAME]",
                    friendly_explanation=f"Oops! You are tracking '{file_name}'. {reason}.",
                    remediation_steps=[
                        f"Add '{file_name}' to your .gitignore file.",
                        f"Run 'git rm --cached {file_path}' to stop Git from tracking it without deleting your local copy.",
                        "Commit the removal and push safely.",
                    ],
                )
        return None

    def scan_text(self, text: str, file_path: str = "inline_code") -> List[SecretFinding]:
        """Scans raw file content line by line."""
        findings: List[SecretFinding] = []
        path_finding = self.audit_file_path(file_path)
        if path_finding:
            findings.append(path_finding)

        lines = text.splitlines()
        for line_idx, line in enumerate(lines, start=1):
            findings.extend(self._scan_single_line(line, line_idx, file_path))

        return findings

    def scan_git_diff(self, diff_text: str) -> List[SecretFinding]:
        """
        Parses a unified git diff format (+ lines only) and extracts file paths,
        line numbers, and secret findings.
        """
        findings: List[SecretFinding] = []
        current_file = "unknown_file"
        current_line_num = 0

        # Pattern for diff header: +++ b/path/to/file.py
        file_header_pattern = re.compile(r"^\+\+\+\s+b/(.*)$")
        # Pattern for hunk header: @@ -1,4 +10,6 @@
        hunk_header_pattern = re.compile(r"^@@\s+-\d+(?:,\d+)?\s+\+(\d+)(?:,\d+)?\s+@@")

        for line in diff_text.splitlines():
            # Check for target file in diff
            file_match = file_header_pattern.match(line)
            if file_match:
                current_file = file_match.group(1).strip()
                path_alert = self.audit_file_path(current_file)
                if path_alert:
                    findings.append(path_alert)
                continue

            # Check for hunk header to track line numbers accurately
            hunk_match = hunk_header_pattern.match(line)
            if hunk_match:
                current_line_num = int(hunk_match.group(1)) - 1
                continue

            # Only analyze added lines (starting with + but not +++)
            if line.startswith("+") and not line.startswith("+++"):
                current_line_num += 1
                added_content = line[1:]
                line_findings = self._scan_single_line(added_content, current_line_num, current_file)
                findings.extend(line_findings)
            elif not line.startswith("-"):
                # Context line: increment line number
                current_line_num += 1

        return findings

    def _scan_single_line(self, line: str, line_number: int, file_path: str) -> List[SecretFinding]:
        findings: List[SecretFinding] = []
        stripped = line.strip()

        # Skip comment lines that explicitly describe documentation examples
        if stripped.startswith(("#", "//", "/*", "*", "<!--")) and any(
            marker in stripped.lower() for marker in ["e.g.", "for example", "placeholder", "your_key_here"]
        ):
            return []

        # 1. Check known regex signatures
        for rule_id, rule_name, severity, pattern, explanation in self.KNOWN_PATTERNS:
            for match in pattern.finditer(line):
                matched_secret = match.group(1) if match.groups() else match.group(0)
                findings.append(
                    SecretFinding(
                        rule_id=rule_id,
                        rule_name=rule_name,
                        severity=severity,
                        file_path=file_path,
                        line_number=line_number,
                        raw_match=matched_secret,
                        masked_value=self.mask_secret(matched_secret),
                        friendly_explanation=explanation,
                        remediation_steps=[
                            "Move this secret to your local .env file (e.g. MY_KEY=value).",
                            "Read it in code via environment variables (e.g. process.env or os.getenv).",
                            "If this was pushed publicly, revoke and regenerate the key immediately!",
                        ],
                    )
                )

        # 2. Heuristic check: High Shannon entropy in key assignments
        assignment_pattern = re.compile(
            r"""(?i)(?:api_key|token|secret|password|auth_key|private_key)\s*[:=]\s*['"]([^'"]{20,})['"]"""
        )
        for match in assignment_pattern.finditer(line):
            candidate = match.group(1)
            # Avoid duplicate if already caught by a known signature
            if any(f.raw_match == candidate for f in findings):
                continue

            entropy = self.calculate_shannon_entropy(candidate)
            # Threshold: Random tokens typically have entropy > 4.0
            if entropy >= 4.0 and len(candidate) >= 20:
                findings.append(
                    SecretFinding(
                        rule_id="HIGH_ENTROPY_TOKEN",
                        rule_name="Unidentified High-Entropy Secret",
                        severity=Severity.HIGH,
                        file_path=file_path,
                        line_number=line_number,
                        raw_match=candidate,
                        masked_value=self.mask_secret(candidate),
                        friendly_explanation=(
                            "This string looks like a randomly generated secret token or password with very high entropy. "
                            "It should not be hardcoded in your source code."
                        ),
                        remediation_steps=[
                            "Store this variable inside an ignored .env file.",
                            "Access it via process.env or os.environ in your application runtime.",
                        ],
                        entropy=entropy,
                    )
                )

        return findings
