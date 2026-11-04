---
name: vibelog-human-changelog
description: Translates cryptic Git diffs and commit histories into empathetic, plain-English release notes and categorized changelogs ("No-Jargon Mode").
origin: GNT
---

# ✨ VibeLog Human Changelog (`vibelog-human-changelog`)

Converts raw `git diff` hunks into structured, human-friendly release notes categorized by impact.

## When to Activate
- When summarizing a Pull Request or release for non-technical stakeholders or teammates
- When generating `CHANGELOG.md` entries from recent commits
- Via the FastMCP tool `explain_diff`

## Core Capabilities (`core/vibelog.py`)
1. **Semantic Categorization:** Groups changes into `✨ New Features & Upgrades`, `🐛 Fixes & Polishing`, `⚠️ Heads Up (Breaking Changes)`, and `🧹 Behind the Scenes`.
2. **No-Jargon Mode:** Explains what changed and why it matters without intimidating Git internals.

## Usage Example
```python
from core.vibelog import generate_vibelog

summary = generate_vibelog(raw_git_diff)
print(summary.no_jargon_summary)
print(summary.markdown_report)
```
