"""
GNT Model Context Protocol (MCP) Server.
Exposes GitHub Noob Toolkit safety and repair functions as AI tools for Cursor,
Claude Desktop, Windsurf, and modern developer environments.
"""

from __future__ import annotations
import json
import os
import sys
from typing import Optional

# Support both MCP 2.x (MCPServer) and MCP 1.x (FastMCP)
try:
    from mcp.server.mcpserver import MCPServer as FastMCP
except ImportError:
    try:
        from mcp.server.fastmcp import FastMCP
    except ImportError:
        # Fallback dummy class if running without mcp package
        class FastMCP:  # type: ignore
            def __init__(self, name: str, **kwargs):
                self.name = name
            def tool(self):
                def decorator(fn):
                    return fn
                return decorator
            def run(self):
                pass

from core.secrets import SecretShield
from core.docgen import DocGen, ProjectAnalysis
from core.vibelog import VibeLog
from core.conflicts import ConflictSolver, ConflictResolutionStrategy
from core.dependencies import DepDoctor
from core.health_score import VibeHealthScore


def create_mcp_server() -> FastMCP:
    """Instantiates and registers all GNT tools on the MCP server."""
    server = FastMCP(
        "GitHub-Noob-Toolkit",
        instructions=(
            "GNT is an automated protective shield and repair copilot for beginners and vibe coders. "
            "Use its tools to check for exposed secrets, explain diffs without confusing jargon, "
            "resolve merge conflicts, generate simple READMEs, and fix missing dependencies."
        ),
    )

    shield = SecretShield()

    @server.tool()
    def scan_code_for_leaks(code_or_diff: str, file_path: str = "code_snippet.py") -> str:
        """
        Scans code or git diffs for leaked secrets (OpenAI, Stripe, AWS, SSH keys, passwords,
        high-entropy strings) and checks if sensitive files like .env are tracked.
        """
        if "diff --git" in code_or_diff or code_or_diff.startswith("---") or "\n+" in code_or_diff:
            findings = shield.scan_git_diff(code_or_diff)
        else:
            findings = shield.scan_text(code_or_diff, file_path=file_path)

        if not findings:
            return json.dumps(
                {
                    "status": "clean",
                    "message": "Shield Clear! No secret leaks or sensitive files found. Safe to commit! ✨",
                    "findings": [],
                },
                indent=2,
            )

        return json.dumps(
            {
                "status": "leaks_detected",
                "message": f"Found {len(findings)} exposed secret(s). Follow the remediation steps to fix them safely.",
                "findings": [f.to_dict() for f in findings],
            },
            indent=2,
        )

    @server.tool()
    def generate_simple_readme(
        project_name: str,
        project_type: str = "Full-Stack Web App",
        primary_language: str = "TypeScript",
        install_command: str = "npm install",
        run_command: str = "npm run dev",
        env_vars_comma_separated: str = "",
    ) -> str:
        """
        Generates a clean, friendly, jargon-free README.md with clear quickstart steps
        and an environment variables setup table.
        """
        env_list = [v.strip() for v in env_vars_comma_separated.split(",") if v.strip()]
        analysis = ProjectAnalysis(
            project_name=project_name,
            project_type=project_type,
            primary_language=primary_language,
            package_manager=install_command.split()[0] if install_command else "npm",
            install_commands=[install_command],
            run_commands=[run_command],
            detected_dependencies=[],
            detected_env_vars=env_list,
            has_docker=False,
        )
        return DocGen.generate_readme(analysis)

    @server.tool()
    def explain_diff(diff: str, commit_message: str = "") -> str:
        """
        Translates a technical Git diff into a friendly, human-readable changelog with
        Features ✨, Fixes 🐛, and an empathetic 'No-Jargon' summary.
        """
        summary = VibeLog.parse_diff(diff, commit_message=commit_message or None)
        return summary.to_markdown()

    @server.tool()
    def resolve_conflict(conflict_content: str, strategy: str = "smart_hybrid") -> str:
        """
        Parses merge conflict markers (<<<<<<< HEAD, =======, >>>>>>>) and returns
        both an empathetic explanation and the clean, resolved file content.
        Strategy options: 'smart_hybrid' (recommended), 'ours', or 'theirs'.
        """
        strat_enum = ConflictResolutionStrategy(strategy) if strategy in ("ours", "theirs", "smart_hybrid") else ConflictResolutionStrategy.SMART_HYBRID
        analysis = ConflictSolver.analyze_file_content(conflict_content)

        if not analysis.has_conflicts:
            return json.dumps({"has_conflicts": False, "message": "No merge conflicts detected!"})

        resolved_text = ConflictSolver.resolve_conflicts(conflict_content, default_strategy=strat_enum)

        return json.dumps(
            {
                "has_conflicts": True,
                "total_conflicts": analysis.total_conflicts,
                "summary": analysis.summary_message,
                "blocks": [b.to_dict() for b in analysis.blocks],
                "resolved_code": resolved_text,
            },
            indent=2,
        )

    @server.tool()
    def detect_missing_dependencies(code: str, manifest: str = "", manifest_type: str = "python") -> str:
        """
        Finds packages imported in code that are missing from requirements.txt or package.json.
        Returns the missing libraries and an auto-repaired manifest patch.
        """
        if manifest_type == "python":
            findings = DepDoctor.audit_python_repository({"app.py": code}, requirements_content=manifest)
            patched_manifest = DepDoctor.generate_manifest_patch(findings, manifest, manifest_type="python_requirements")
        else:
            findings = DepDoctor.audit_node_repository({"app.ts": code}, package_json_content=manifest)
            patched_manifest = DepDoctor.generate_manifest_patch(findings, manifest, manifest_type="node_package_json")

        return json.dumps(
            {
                "missing_count": len(findings),
                "findings": [f.to_dict() for f in findings],
                "patched_manifest": patched_manifest,
            },
            indent=2,
        )

    @server.tool()
    def calculate_vibe_score(
        critical_leaks: int = 0,
        high_leaks: int = 0,
        forbidden_files: int = 0,
        has_readme: bool = True,
        conflicts: int = 0,
        missing_deps: int = 0,
    ) -> str:
        """
        Calculates the repository Vibe Health Score (0-100) with visual color and advice.
        """
        res = VibeHealthScore.calculate(
            critical_secrets_count=critical_leaks,
            high_secrets_count=high_leaks,
            forbidden_files_count=forbidden_files,
            has_readme=has_readme,
            active_conflicts_count=conflicts,
            missing_dependencies_count=missing_deps,
        )
        return json.dumps(res.to_dict(), indent=2)

    return server


mcp = create_mcp_server()

if __name__ == "__main__":
    # When run directly via `python -m mcp_server.server`
    print("Starting GNT MCP Server (stdio transport)...", file=sys.stderr)
    mcp.run()
