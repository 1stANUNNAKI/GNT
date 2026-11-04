# Contributing to GitHub Noob Toolkit (GNT)

Thanks for contributing to **GitHub Noob Toolkit (GNT)** — the automated protective shield, documentation architect, and FastMCP copilot for beginners and AI vibe coders!

## Table of Contents

- [What We're Looking For](#what-were-looking-for)
- [Quick Start](#quick-start)
- [Contributing Skills (`skills/`)](#contributing-skills-skills)
- [Contributing Agents (`agents/`)](#contributing-agents-agents)
- [Contributing Commands (`commands/`)](#contributing-commands-commands)
- [Contributing Core Engine Modules (`core/`)](#contributing-core-engine-modules-core)
- [Cross-Harness Skill Discovery](#cross-harness-skill-discovery)
- [Pull Request Process & Pre-Push Gauntlet](#pull-request-process--pre-push-gauntlet)

---

## What We're Looking For

### 1. Skills (`skills/<skill-name>/SKILL.md`)
Reusable AI agent workflows and domain playbooks:
- Secret detection and security hardening workflows
- Automated documentation and repository governance (`git-docs-architect`)
- Dependency auditing and build error recovery
- Git conflict resolution and beginner-friendly Git guides

### 2. Agents (`agents/<agent-name>.md`)
Specialized subagents invoked for targeted tasks:
- Security & secret-leak reviewers
- Merge conflict healers
- Documentation & Community Health architects
- Dependency & build doctors

### 3. Core Engine & FastMCP Tools (`core/` & `mcp_server/`)
Zero-dependency or lightweight Python modules with 100% unit-test coverage in `tests/`:
- New regex/entropy detectors in `core/secrets.py`
- Additional framework detectors in `core/docgen.py` and `core/dependencies.py`
- New MCP tools exposed in `mcp_server/server.py`

---

## Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/1stANUNNAKI/GNT.git
cd GNT

# 2. Create a feature branch
git checkout -b feat/my-new-skill

# 3. Set up virtual environment & install dependencies
python -m venv .venv
source .venv/bin/activate  # Windows: .\.venv\Scripts\activate
pip install -r requirements.txt

# 4. Run the verification test suite
pytest -v

# 5. Commit and open a Pull Request
git add . && git commit -m "feat(skills): add my-new-skill" && git push -u origin feat/my-new-skill
```

---

## Contributing Skills (`skills/`)

Skills are self-contained workflow modules loaded on demand by Claude Code, Antigravity, Cursor, OpenCode, and Codex.

### Directory Structure
```text
skills/
└── your-skill-name/
    └── SKILL.md
```

### `SKILL.md` Template
```markdown
---
name: your-skill-name
description: Single-line specific description used for auto-activation
origin: GNT
---

# Skill Title

Brief overview of what this skill accomplishes.

## When to Activate
- Clear trigger conditions when the AI agent should load this skill.

## Core Capabilities
1. First capability
2. Second capability

## Usage Example
\`\`\`python
# Practical, tested example
\`\`\`

## Anti-Patterns
- What NOT to do.
```

### Skill Checklist
- [ ] Focused on one clear workflow or domain
- [ ] Frontmatter `name:` matches the parent directory name (`^[a-z0-9]+(-[a-z0-9]+)*$`)
- [ ] Frontmatter `description:` is a single-line string (no multiline block scalars)
- [ ] Includes `When to Activate` and practical code examples
- [ ] Zero hardcoded secrets, API keys, or personal paths
- [ ] Mirrored into `.agents/skills/<skill-name>/SKILL.md` for cross-harness discovery

---

## Contributing Agents (`agents/`)

Agents live in `agents/your-agent-name.md` and define specialized roles:

```markdown
---
name: your-agent-name
description: Specific description of what this agent does and when to invoke it.
tools: Read, Write, Edit, Bash, Grep, Glob
model: sonnet
---

You are a [role] specialist.

## Your Role
- Primary responsibility
- Boundaries (what you do not do)

## Workflow
1. Step 1: Analyze
2. Step 2: Execute
3. Step 3: Verify
```

---

## Contributing Commands (`commands/`)

Slash commands live in `commands/your-command.md`:

```markdown
---
description: Brief description shown in /help
---

# `/your-command` — Title

## Purpose
What this command executes.

## Usage
\`\`\`text
/your-command [arguments]
\`\`\`
```

---

## Contributing Core Engine Modules (`core/`)

Every function added to `core/` must adhere to Clean Code standards:
1. **Single Responsibility (SRP):** Keep functions focused and concise.
2. **Fail Fast & Guard Clauses:** Validate inputs immediately at the top of each function.
3. **Unit Tests Required:** Add comprehensive tests under `tests/test_<module>.py` and verify with `pytest -v`.

---

## Cross-Harness Skill Discovery

When adding a new skill under `skills/<skill-name>/SKILL.md`, also copy it to `.agents/skills/<skill-name>/SKILL.md` so both `agentskills.io`-compliant tools (Antigravity, OpenCode, Codex, Cursor) and Claude Code discover it automatically.

---

## Pull Request Process & Pre-Push Gauntlet

### 1. PR Title Format (Conventional Commits)
- `feat(skills): add git-docs-architect skill`
- `feat(core): add GCP service account detector to secrets shield`
- `fix(conflicts): preserve trailing newline in hybrid merge`
- `docs(readme): synchronize English and Arabic skill tables`

### 2. Before You Push (Mandatory Verification)
Run the test suite locally before pushing:
```bash
pytest -v
```
Ensure all tests pass (`25 passed`) and zero secrets exist in any staged file.
