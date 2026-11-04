# 🎯 GitHub Noob Toolkit (GNT) — Real-World Use Cases & Workflow Playbook

> **Language:** [🇬🇧 English](../../README.md) | [🇸🇦 العربية](../../README_AR.md)

This playbook details **6 real-world engineering scenarios** showing how beginners, AI vibe coders, and software teams use **GNT's 8 Skills, 4 Agents, 5 Slash Commands, and FastMCP Server** in daily development.

---

## 🛡️ Use Case 1: Pre-Push Secret Leak Interception
**Scenario:** You just built an AI app in Cursor or Claude Code and are about to push your code to a public GitHub repository, unaware that an `sk-proj-...` OpenAI key or high-entropy database password was left in `config.py` or `.env`.
- **Skill Used:** [`secret-leak-shield`](../../skills/secret-leak-shield/SKILL.md)
- **Slash Command:** `/gnt-scan`
- **MCP Tool:** `scan_code_for_leaks`
- **How GNT Solves It:**
  1. Scans every added line using deterministic regex rules + Shannon Entropy ($H \ge 4.0$).
  2. Flags forbidden files (`.env`, `id_rsa`) if staged.
  3. Masks the leaked secret (`sk-p...9x`) and provides the exact `.gitignore` and `os.environ.get()` fix before the push occurs.

---

## ⚔️ Use Case 2: One-Click Branch Merge Conflict Healing
**Scenario:** Git outputs `CONFLICT (content): Merge conflict in app/main.py` and fills your file with `<<<<<<< HEAD`, `=======`, and `>>>>>>> feature-branch` markers.
- **Skill Used:** [`smart-conflict-solver`](../../skills/smart-conflict-solver/SKILL.md)
- **Slash Command:** `/gnt-heal`
- **MCP Tool:** `resolve_conflict`
- **How GNT Solves It:**
  1. Parses all conflict blocks in memory without corrupting surrounding code.
  2. Applies the **Smart Hybrid Merge** strategy to combine non-overlapping imports and functions from both branches.
  3. Explains what was kept from each branch in plain, jargon-free English.

---

## 🩺 Use Case 3: Pre-Deployment Dependency Audit (`ModuleNotFoundError` Prevention)
**Scenario:** Your app works on your laptop (because packages were installed globally), but deploying to Render, Railway, or Docker crashes immediately with `ModuleNotFoundError: No module named 'stripe'`.
- **Skill Used:** [`dep-doctor-scanner`](../../skills/dep-doctor-scanner/SKILL.md)
- **Slash Command:** `/gnt-deps`
- **MCP Tool:** `detect_missing_dependencies`
- **How GNT Solves It:**
  1. Parses all `.py` files with Python's Abstract Syntax Tree (`ast.parse`).
  2. Filters out Python standard library modules (`os`, `sys`, `json`, `pathlib`, etc.) and compares third-party imports against `requirements.txt`.
  3. Generates the exact missing lines (`stripe>=8.0.0`) to append to `requirements.txt`.

---

## 🏛️ Use Case 4: Upgrading Any Repo to 100% GitHub Community Health (ECC Standard)
**Scenario:** You want your repository to display GitHub's official `📖 Readme`, `🤝 Code of conduct`, `⚖️ MIT license`, and `🛡️ Security` navigation tabs, bilingual English/Arabic documentation, and modular AI skills.
- **Skill Used:** [`git-docs-architect`](../../skills/git-docs-architect/SKILL.md)
- **Slash Command:** `/gnt-docs`
- **MCP Tool:** `generate_simple_readme`
- **How GNT Solves It:**
  1. Generates or upgrades `README.md` (English primary), `README_AR.md` (Arabic secondary), `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, `LICENSE`, `SECURITY.md`, `AGENTS.md`, `CHANGELOG.md`, and `TROUBLESHOOTING.md`.
  2. Configures `.gitattributes` and GitHub Repository Topics for maximum search discoverability.

---

## ✨ Use Case 5: Translating Complex Git Diffs into Human Release Notes
**Scenario:** You need to share what changed in a 40-file Pull Request with users, clients, or teammates without dumping raw commit hashes and diff hunks.
- **Skill Used:** [`vibelog-human-changelog`](../../skills/vibelog-human-changelog/SKILL.md)
- **MCP Tool:** `explain_diff`
- **How GNT Solves It:**
  1. Categorizes diffs into `✨ New Features`, `🐛 Fixes`, `⚠️ Heads Up`, and `🧹 Maintenance`.
  2. Produces a warm, empathetic **"No-Jargon Summary"** ready for release notes or Discord/Slack announcements.

---

## 📊 Use Case 6: Automated Pull Request Gate via GitHub App Checks API
**Scenario:** You want every Pull Request opened on your repositories to be automatically scored from `0` to `100` (`Grade A+` to `F`) and blocked if secrets are leaked.
- **Skill Used:** [`vibe-health-scorer`](../../skills/vibe-health-scorer/SKILL.md) + `github_app/webhook_handler.py`
- **Slash Command:** `/gnt-score`
- **How GNT Solves It:**
  1. Receives `push` and `pull_request` webhooks verified by HMAC-SHA256 (`X-Hub-Signature-256`).
  2. Runs all 5 core engines and posts an inline Checks API run + friendly PR review comment with the `0-100` Vibe Health Score.
