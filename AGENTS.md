# GitHub Noob Toolkit (GNT) — Agent Instructions (`AGENTS.md`)

This repository is a **full-stack protective copilot, FastMCP server, and AI skill suite** providing **8 specialized skills, 4 agents, 5 slash commands, and 6 core safety engines** for developers and AI vibe coders.

**Version:** 2.0.0

---

## Core Principles

1. **Security-First (`Zero-Leak Guarantee`)** — Never allow API keys, PATs, or `.env` files to be committed; always run `secret-leak-shield` (`core/secrets.py`) before commits.
2. **No-Jargon Empathy** — Explain every Git operation, diff, and merge conflict in clear, beginner-friendly language alongside technical details.
3. **Test-Driven Verification** — Maintain 100% passing unit tests (`pytest -v`) across all core modules, webhooks, and billing services.
4. **Clean Code & Guard Clauses** — Keep functions modular (SRP), use early returns, and never mutate input structures unexpectedly.
5. **Bilingual Documentation Parity** — Keep `README.md` (Primary English) and `README_AR.md` (Secondary Arabic) synchronized at all times.

---

## Available Agents (`agents/`)

| Agent | File | Purpose | When to Use |
| :--- | :--- | :--- | :--- |
| `gnt-security-auditor` | [`agents/gnt-security-auditor.md`](./agents/gnt-security-auditor.md) | Dual-layer Regex + Shannon Entropy secret scanning | Before commits, PR reviews, or publishing Gists |
| `gnt-conflict-healer` | [`agents/gnt-conflict-healer.md`](./agents/gnt-conflict-healer.md) | 3-strategy Git merge conflict resolution (`hybrid`, `ours`, `theirs`) | When conflict markers (`<<<<<<< HEAD`) appear |
| `gnt-docs-architect` | [`agents/gnt-docs-architect.md`](./agents/gnt-docs-architect.md) | ECC-grade GitHub documentation & Community Health tabs | Creating or updating repo docs (`README`, `SECURITY`, etc.) |
| `gnt-dep-doctor` | [`agents/gnt-dep-doctor.md`](./agents/gnt-dep-doctor.md) | AST import analysis & manifest patching (`requirements.txt` / `package.json`) | Before deployment or after adding new imports |

---

## Available Skills (`skills/` & `.agents/skills/`)

| # | Skill Name | Directory | Core Module / Engine | Primary Use Case |
| :-: | :--- | :--- | :--- | :--- |
| **01** | `git-docs-architect` | [`skills/git-docs-architect/`](./skills/git-docs-architect/SKILL.md) | `core/docgen.py` + Templates | Build full ECC-grade GitHub docs (`README`, `SECURITY`, `CONTRIBUTING`, `CODE_OF_CONDUCT`, `LICENSE`) |
| **02** | `secret-leak-shield` | [`skills/secret-leak-shield/`](./skills/secret-leak-shield/SKILL.md) | `core/secrets.py` | Scan code & diffs for API keys, PATs, high-entropy strings, and `.env` files |
| **03** | `auto-readme-docgen` | [`skills/auto-readme-docgen/`](./skills/auto-readme-docgen/SKILL.md) | `core/docgen.py` | Auto-generate beginner-friendly 3-step `README.md` from project manifests |
| **04** | `vibelog-human-changelog` | [`skills/vibelog-human-changelog/`](./skills/vibelog-human-changelog/SKILL.md) | `core/vibelog.py` | Translate Git diffs into categorized, plain-English release notes |
| **05** | `smart-conflict-solver` | [`skills/smart-conflict-solver/`](./skills/smart-conflict-solver/SKILL.md) | `core/conflicts.py` | Resolve `<<<<<<< HEAD` merge conflicts via Smart Hybrid Merge |
| **06** | `dep-doctor-scanner` | [`skills/dep-doctor-scanner/`](./skills/dep-doctor-scanner/SKILL.md) | `core/dependencies.py` | Detect undeclared Python/JS imports via AST and patch manifests |
| **07** | `vibe-health-scorer` | [`skills/vibe-health-scorer/`](./skills/vibe-health-scorer/SKILL.md) | `core/health_score.py` | Calculate `0-100` repository health score and `A+`..`F` grade |
| **08** | `fastmcp-ide-bridge` | [`skills/fastmcp-ide-bridge/`](./skills/fastmcp-ide-bridge/SKILL.md) | `mcp_server/server.py` | Expose all 6 GNT engines as native MCP tools in Cursor, Claude & Antigravity |

---

## Security Guidelines (Before ANY Commit)

- Zero hardcoded secrets (`sk-`, `ghp_`, `github_pat_`, `AKIA`, `sk_live_`) in any file.
- Verify webhook signatures (`HMAC-SHA256`) on all GitHub App and Stripe endpoints.
- Mask any detected secret preview via `core.secrets.mask_secret()`.
- Run `pytest -v` and confirm all 25 unit tests pass.

---

## Project Structure

```text
GNT/
├── agents/          # 4 specialized subagents (Security, Conflicts, Docs, Dependencies)
├── skills/          # 8 modular AI workflow skills (including git-docs-architect)
├── .agents/skills/  # Cross-harness skill discovery mirror (Codex, Cursor, Antigravity, OpenCode)
├── commands/        # 5 slash commands (/gnt-scan, /gnt-docs, /gnt-heal, /gnt-deps, /gnt-score)
├── core/            # 6 Python safety & automation engines (secrets, docgen, vibelog, conflicts, dependencies, health_score)
├── mcp_server/      # FastMCP server exposing 6 native IDE tools
├── github_app/      # GitHub App webhook handler, Checks API runner, and PR commenter
├── backend/         # FastAPI REST API, SQLAlchemy 2.0 AsyncPG models, and Stripe billing
├── frontend/        # Next.js 14 App Router SaaS dashboard & interactive Playground
├── docs/use-cases/  # Real-world engineering use-cases playbook
└── tests/           # 25 Pytest unit and integration tests
```
