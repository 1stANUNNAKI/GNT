---
name: git-docs-architect
description: Engineers production-grade GitHub repository documentation, Community Health tabs (README.md, README_AR.md, CODE_OF_CONDUCT.md, CONTRIBUTING.md, LICENSE, SECURITY.md, AGENTS.md, CHANGELOG.md, TROUBLESHOOTING.md), and decomposes software projects into modular AI skills, agents, and use-case playbooks following the ECC methodology.
origin: GNT / ANUNNAKI Council
---

# 🏛️ Git Docs & Governance Architect (`git-docs-architect`)

An enterprise documentation and repository restructuring skill modeled after the **ECC (`Everything Claude Code`)** and **ANUNNAKI Council** standard. It transforms any raw or partially documented codebase into a 100% GitHub Community Health compliant, skill-modularized, bilingual (English primary + Arabic secondary) open-source or private engineering repository.

---

## 🎯 When to Activate

Activate this skill whenever the user asks to:
- Upgrade, standardize, or organize a GitHub repository's documentation (`README.md`, `SECURITY.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `LICENSE`, `AGENTS.md`, `CHANGELOG.md`, `TROUBLESHOOTING.md`).
- Activate GitHub's top Community Health navigation tabs (`📖 Readme`, `🤝 Code of conduct`, `⚖️ MIT license`, `🛡️ Security`).
- Reorganize a project into modular AI Skills (`skills/<name>/SKILL.md`), Subagents (`agents/<name>.md`), Slash Commands (`commands/<name>.md`), and Use-Case Playbooks (`docs/use-cases/`).
- Enforce the Mandatory Repository Identity Standard (`Topics`, `Languages & Tech Stack Badges`, `.gitattributes`, and `MIT License`).

---

## 🧬 The ECC Documentation & Governance Methodology (Deep-Dive Blueprint)

GitHub automatically inspects the root directory (and `.github/`) of every repository to render the **Community Health Navigation Bar** at the top of the repository overview:

```text
[ 📖 Readme ]  [ 🤝 Code of conduct ]  [ ⚖️ MIT license ]  [ 🛡️ Security ]
```

To unlock all 4 tabs and achieve a 100% Community Health score, the repository MUST contain the following canonical files engineered with specific structural sections:

### 1. `README.md` (Primary English) & `README_AR.md` (Secondary Arabic)
A world-class ECC-grade `README.md` follows a strict 10-zone visual and cognitive hierarchy:
1. **Zone 1 — Language Switcher & Governance Badges:**
   - Top centered badges switching between `README.md` (English Primary) and `README_AR.md` (Arabic Secondary), plus `License: MIT` and Security/Test status badges.
2. **Zone 2 — Tech Stack & Languages Pill Bar (`Built With`):**
   - Shields.io badges for every programming language, framework, database, and protocol used in the repository (matched with `.gitattributes` so GitHub Linguist displays the same languages in the sidebar bar).
3. **Zone 3 — Official Sources & Trust Boundary Callout (`> [!WARNING]`):**
   - Explicit notice listing official repository URLs, packages, and endpoints to prevent supply-chain spoofing.
4. **Zone 4 — One-Line Value Proposition & Execution Pipeline:**
   - A concise ASCII pipeline (`plan -> scan -> heal -> document -> verify -> deploy`) + a **Summary Value Table** (`Included | Count | What it gives you`).
5. **Zone 5 — Architecture Diagram (`Mermaid`):**
   - Clean `flowchart TD` or `flowchart LR` showing how user interfaces, CLI/MCP surfaces, core engines, and storage layers interact.
6. **Zone 6 — Modular Skills & Use-Cases Matrix (`Start Using`):**
   - Task-oriented routing table (`What you are doing | Start here (Skill / Command) | Underlying Module`) so users start with the workflow they need rather than reading the entire codebase.
7. **Zone 7 — Guided Setup & Multi-Runner Installation:**
   - Copy-pasteable setup blocks for `pnpm` / `npm` / `uv` / `pip` / `Docker Compose`, with `<details>` collapsible sections for advanced or per-harness options (`Claude Code`, `Cursor`, `Antigravity`, `OpenCode`, `Codex`).
8. **Zone 8 — Annotated Component & Skills Directory Tree (`What's Inside`):**
   - Visual ASCII tree explaining the role of `skills/`, `agents/`, `commands/`, `core/`, `backend/`, `frontend/`, `mcp_server/`, and `tests/`.
9. **Zone 9 — Operational Verification (`verify: PASS`):**
   - Exact test suite commands (`pytest -v`, `pnpm test`) and verified passing output.
10. **Zone 10 — License & Attribution:**
    - Direct link to [`LICENSE`](./LICENSE) (`MIT License`).

---

### 2. `CODE_OF_CONDUCT.md` (Activates the `Code of conduct` Tab)
Engineered using the **Contributor Covenant v2.0** specification and **Mozilla's 4-Stage Enforcement Ladder**:
- **`## Our Pledge`**: Commitment to a harassment-free, inclusive engineering community.
- **`## Our Standards`**: Positive behaviors (empathy, constructive feedback, responsibility) vs. unacceptable behaviors (trolling, harassment, publishing private data/tokens).
- **`## Enforcement Responsibilities & Scope`**: Maintainer rights to review/remove non-compliant PRs, issues, or comments across all project spaces.
- **`## Enforcement Guidelines (The 4-Stage Ladder)`**:
  1. `### 1. Correction` (Private written warning + clarity)
  2. `### 2. Warning` (Formal warning + temporary interaction restriction)
  3. `### 3. Temporary Ban` (Timed suspension from all community interaction)
  4. `### 4. Permanent Ban` (Permanent removal for sustained or severe violations)
- **`## Attribution`**: Link to Contributor Covenant v2.0 (`https://www.contributor-covenant.org/version/2/0/code_of_conduct.html`).

---

### 3. `SECURITY.md` (Activates the `Security` Tab — `?tab=security-ov-file`)
Engineered as a rigorous **Supply-Chain & Trust-Boundary Security Policy**:
- **`## Supported Versions`**: Markdown table showing which release branches receive active security patches (`:white_check_mark:` vs `:x:`).
- **`## Reporting a Vulnerability`**:
  - Direct link to **GitHub Private Vulnerability Reporting** (`https://github.com/<owner>/<repo>/security/advisories/new`).
  - Explicit warning: **Do NOT open a public GitHub issue for security vulnerabilities.**
  - Required reproduction payload (affected file/version/commit, clean-checkout reproduction steps, trust boundary crossed, redacted PoC logs).
  - **Response SLA**: Acknowledgment (`within 48 hours`), Initial Assessment (`within 7 days`), Critical Fix (`within 14 days`), and Coordinated Disclosure.
- **`## Scope & Official Distribution Surfaces`**: Exact code directories, APIs, MCP servers, and GitHub Actions covered, plus anti-spoofing package rules.
- **`## Out of Scope`**: Self-XSS, social engineering, or local shell execution where no trust boundary is crossed.
- **`## Supply-Chain Rules`**: Pinned GitHub Actions, zero untrusted interpolation in `run:` blocks, mandatory pre-commit secret scanning.
- **`## Operational Guidance (Secrets Handling & Port Auditing)`**:
  - Never hardcode PATs (`ghp_`), OpenAI (`sk-`), Stripe (`sk_live_`), or AWS (`AKIA`) keys in `.env` or `mcp.json`.
  - Copy-pasteable Bash (`grep -EnH`) and PowerShell (`Select-String`) secret audit commands.
  - Local port PID verification (`netstat -ano` / `lsof -iTCP`).
- **`## Security Resources`**: OWASP Top 10 for Agentic Applications & OWASP MCP Top 10 links.

---

### 4. `CONTRIBUTING.md` (Linked Automatically on New Issues & PRs)
Structured as a modular contributor onboarding manual:
- **`## What We're Looking For`**: Skills, Agents, Core Modules, Hooks, Commands, and Tests.
- **`## Quick Start`**: 5-step `gh repo fork` -> `git checkout -b feat/...` -> implement -> test -> PR flow.
- **`## Contributing Skills (`skills/<name>/SKILL.md`)`**: Directory layout, YAML frontmatter rules (`name` matching folder, single-line `description`), required sections (`When to Activate`, `Core Concepts`, `Code Examples`, `Anti-Patterns`, `Best Practices`), and 11-point Skill Checklist.
- **`## Contributing Agents (`agents/<name>.md`)` & Commands (`commands/<name>.md`)**: Standardized templates.
- **`## Pull Request Process & Pre-Push Verification Gauntlet`**: Conventional Commit PR titles (`feat(skills): ...`, `fix(core): ...`), PR description checklist, and mandatory test execution before pushing.

---

### 5. `LICENSE` (Activates the `MIT license` Tab)
Standard **MIT License** file at the repository root (`Copyright (c) 2026 1stANUNNAKI`), enabling GitHub's `Licensee` parser to display `⚖️ MIT license`.

---

### 6. `AGENTS.md`, `CHANGELOG.md`, and `TROUBLESHOOTING.md`
- **`AGENTS.md`**: Machine-and-human readable instruction sheet for AI coding agents working inside the repo (Core Principles, Available Agents & Skills table, Pre-Commit Security Checklist, Coding Style, 80%+ Test Coverage rule).
- **`CHANGELOG.md`**: Keep-a-Changelog semantic release history (`Added`, `Changed`, `Fixed`, `Security`, `Release Audit`).
- **`TROUBLESHOOTING.md`**: Diagnostic playbook organized by category (`Symptom` -> `Causes` -> copy-pasteable `Solutions` in Bash & PowerShell).

---

## 🛠️ Execution Workflow (Step-by-Step)

When applying `git-docs-architect` to any repository:
1. **Audit Repository Surface:** Inspect all source directories, languages, package manifests (`pyproject.toml`, `package.json`, `requirements.txt`, `Dockerfile`), and test suites.
2. **Decompose into Skills & Use Cases:** Group every core capability into a self-contained skill under `skills/<skill-name>/SKILL.md` (and mirror to `.agents/skills/<skill-name>/SKILL.md`), plus create agent profiles in `agents/` and use-case guides in `docs/use-cases/`.
3. **Generate the 9 Canonical Documentation & Governance Files:** Write `README.md` (English), `README_AR.md` (Arabic), `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, `LICENSE`, `SECURITY.md`, `AGENTS.md`, `CHANGELOG.md`, and `TROUBLESHOOTING.md`.
4. **Configure Linguist & GitHub Templates:** Add `.gitattributes` for accurate language bars, `.github/PULL_REQUEST_TEMPLATE.md`, and apply repository Topics via the GitHub API.
5. **Verify:** Run the test suite and secret scanner to confirm zero broken tests and zero leaked credentials.
