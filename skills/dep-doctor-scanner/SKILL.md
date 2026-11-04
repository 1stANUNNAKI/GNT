---
name: dep-doctor-scanner
description: Uses Python AST parsing and JS/TS import analysis to detect undeclared third-party packages and auto-generate requirements.txt and package.json patches before deployment fails.
origin: GNT
---

# 🩺 DepDoctor AST Dependency Scanner (`dep-doctor-scanner`)

Catches `ModuleNotFoundError` and missing npm packages locally before cloud deployments (Vercel, Render, Docker, Railway) crash.

## When to Activate
- Before deploying a Python or JavaScript/TypeScript project
- After AI code generation sessions that may have introduced new `import` statements without updating `requirements.txt` or `package.json`
- Via the FastMCP tool `detect_missing_dependencies`

## Core Capabilities (`core/dependencies.py`)
1. **Python AST Import Extraction (`ast.parse`):** Distinguishes Python standard library modules (`sys`, `os`, `json`, `pathlib`, etc.) from installable PyPI packages (`fastapi`, `pydantic`, `stripe`, etc.) and maps import names to package names (`sklearn` -> `scikit-learn`, `cv2` -> `opencv-python`).
2. **Manifest Patch Generation:** Outputs ready-to-append lines for `requirements.txt` or `package.json`.

## Usage Example
```python
from core.dependencies import audit_python_dependencies, generate_requirements_patch

report = audit_python_dependencies(source_files={"app.py": "import fastapi\nimport stripe"}, requirements_txt="fastapi>=0.110.0")
patch = generate_requirements_patch(report.missing_packages)
```
