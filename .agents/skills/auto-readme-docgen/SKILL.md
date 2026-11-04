---
name: auto-readme-docgen
description: Analyzes project manifests (package.json, requirements.txt, pyproject.toml, Dockerfile) and generates beginner-friendly, jargon-free README.md files with 3-step quickstarts.
origin: GNT
---

# 📄 Auto-README & DocGen (`auto-readme-docgen`)

Automatically inspects a codebase's dependencies, frameworks, and entry points to synthesize a clean, copy-pasteable `README.md`.

## When to Activate
- When a new repository lacks a `README.md` or has an outdated starter template
- When onboarding non-traditional developers or "Vibe Coders" who need a clear 3-step setup guide
- Via the FastMCP tool `generate_simple_readme`

## Core Capabilities (`core/docgen.py`)
1. **Stack Auto-Detection:** Identifies FastAPI, Flask, Next.js, React, Vite, Express, PostgreSQL, and Docker configurations automatically.
2. **3-Step Setup Synthesis:** Generates exact `Clone -> Install -> Run` commands tailored to the detected stack.
3. **Environment Variable Table Extraction:** Parses `.env.example` to document required configuration keys safely.

## Usage Example
```python
from core.docgen import analyze_project_files, generate_readme_markdown

meta = analyze_project_files(
    project_name="MyVibeApp",
    file_names=["package.json", ".env.example"],
    package_json_content='{"dependencies": {"next": "14.2.0", "react": "18.3.0"}}',
)
readme_md = generate_readme_markdown(meta)
```
