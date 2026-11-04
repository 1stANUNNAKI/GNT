# Changelog

All notable changes to **GitHub Noob Toolkit (GNT)** are documented in this file following [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and Semantic Versioning.

## [2.0.0] - 2026-11-04

### Added
- **ECC-Grade Community Health & Governance Suite:** Added canonical [`CODE_OF_CONDUCT.md`](./CODE_OF_CONDUCT.md), [`CONTRIBUTING.md`](./CONTRIBUTING.md), [`SECURITY.md`](./SECURITY.md), [`AGENTS.md`](./AGENTS.md), [`CHANGELOG.md`](./CHANGELOG.md), [`TROUBLESHOOTING.md`](./TROUBLESHOOTING.md), [`README_AR.md`](./README_AR.md), and `.github/` PR/Issue templates.
- **8 Modular AI Agent Skills (`skills/` & `.agents/skills/`):**
  - `git-docs-architect`: Complete GitHub documentation & Community Health architect skill.
  - `secret-leak-shield`: Dual-layer Regex + Shannon Entropy secret scanner skill.
  - `auto-readme-docgen`: Beginner-friendly 3-step `README.md` generator skill.
  - `vibelog-human-changelog`: Empathy-driven No-Jargon Git diff translator skill.
  - `smart-conflict-solver`: 3-strategy branch merge conflict solver skill.
  - `dep-doctor-scanner`: AST undeclared dependency detector & manifest patcher skill.
  - `vibe-health-scorer`: 0–100 repository health evaluator skill.
  - `fastmcp-ide-bridge`: Model Context Protocol IDE integration skill.
- **4 Specialized Agents (`agents/`):** `gnt-security-auditor`, `gnt-conflict-healer`, `gnt-docs-architect`, and `gnt-dep-doctor`.
- **5 Slash Commands (`commands/`):** `/gnt-scan`, `/gnt-docs`, `/gnt-heal`, `/gnt-deps`, and `/gnt-score`.
- **Real-World Use-Cases Playbook:** Added [`docs/use-cases/USE_CASES_PLAYBOOK.md`](./docs/use-cases/USE_CASES_PLAYBOOK.md).

### Changed
- Re-architected [`README.md`](./README.md) to the 10-zone ECC standard with primary English documentation, secondary Arabic translation ([`README_AR.md`](./README_AR.md)), task-to-skill routing tables, and annotated component trees.

## [1.0.0] - 2026-10-15

### Added
- Initial release of the 6 GNT Core Safety Modules (`core/secrets.py`, `core/docgen.py`, `core/vibelog.py`, `core/conflicts.py`, `core/dependencies.py`, `core/health_score.py`).
- FastAPI SaaS Backend (`backend/`), GitHub App Webhook & Checks API (`github_app/`), FastMCP Server (`mcp_server/`), Next.js 14 Dashboard (`frontend/`), and 25 passing Pytest unit tests (`tests/`).
