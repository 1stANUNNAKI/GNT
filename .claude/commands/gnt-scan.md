---
description: Scan the repository or staged Git diff for leaked API keys, high-entropy secrets, and forbidden tracked files (.env).
---

# `/gnt-scan` — GNT Secret Leak Shield

## Purpose
Executes a dual-layer security scan (deterministic regex + Shannon entropy $H \ge 4.0$) using `core/secrets.py` and `skills/secret-leak-shield/SKILL.md`.

## Usage
```text
/gnt-scan [path-or-diff]
```
