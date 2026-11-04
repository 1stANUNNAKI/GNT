---
description: Scan Python and JS/TS files via AST to find undeclared dependencies and patch requirements.txt or package.json.
---

# `/gnt-deps` — GNT DepDoctor Scanner

## Purpose
Invokes `skills/dep-doctor-scanner/SKILL.md` (`core/dependencies.py`) to prevent `ModuleNotFoundError` in production deployments.

## Usage
```text
/gnt-deps [project-dir]
```
