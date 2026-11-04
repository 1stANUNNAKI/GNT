---
name: fastmcp-ide-bridge
description: Exposes all GNT protective capabilities (secret scanning, auto-README, diff explanation, conflict healing, dependency auditing, and health scoring) as native Model Context Protocol (FastMCP) tools for Claude Code, Cursor, Windsurf, and Antigravity.
origin: GNT
---

# 🔌 FastMCP IDE Bridge (`fastmcp-ide-bridge`)

Connects the GNT Core Engine directly into any MCP-compatible AI coding environment via `mcp_server/server.py`.

## Exposed MCP Tools
| Tool Name | Input Parameters | Output |
| :--- | :--- | :--- |
| `scan_code_for_leaks` | `diff_text: str`, `tracked_files: list[str]` | Secret findings, severity, masked previews, and remediation steps |
| `generate_simple_readme` | `project_name: str`, `file_names: list[str]` | Complete beginner-friendly `README.md` |
| `explain_diff` | `diff_text: str` | Categorized human changelog + No-Jargon summary |
| `resolve_conflict` | `conflicted_text: str`, `strategy: str` | Clean merged code + explanation |
| `detect_missing_dependencies` | `python_code: str`, `requirements_txt: str` | Missing PyPI packages + `requirements.txt` patch |
| `calculate_vibe_score` | `secret_count`, `has_readme`, `missing_deps_count`, `has_conflicts` | `0-100` score, grade (`A+`..`F`), and action checklist |
