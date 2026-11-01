"""
Auto-README & DocGen Module.
Analyzes repository dependencies, manifests, and project structure to generate
crystal-clear, jargon-free READMEs and setup guides for beginners and vibe coders.
"""

from __future__ import annotations
import json
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class ProjectAnalysis:
    project_name: str
    project_type: str  # e.g., "Next.js App", "FastAPI Service", "Node Backend"
    primary_language: str
    package_manager: str  # "npm", "pnpm", "yarn", "pip", "poetry"
    run_commands: List[str]
    install_commands: List[str]
    detected_dependencies: List[str]
    detected_env_vars: List[str] = field(default_factory=list)
    has_docker: bool = False


class DocGen:
    """
    Intelligently generates beautiful, friendly, beginner-proof documentation.
    Eliminates confusing jargon and provides ready-to-run terminal commands.
    """

    @classmethod
    def analyze_project_files(
        cls,
        files: Dict[str, str],
        default_name: str = "My Awesome App",
    ) -> ProjectAnalysis:
        """
        Takes a mapping of {filepath: file_content} and auto-detects the project profile.
        """
        project_name = default_name
        project_type = "Full-Stack Application"
        primary_language = "JavaScript / TypeScript"
        package_manager = "npm"
        install_commands = ["npm install"]
        run_commands = ["npm run dev"]
        dependencies: List[str] = []
        env_vars: List[str] = []
        has_docker = "Dockerfile" in files or "docker-compose.yml" in files

        # 1. Inspect package.json
        if "package.json" in files:
            try:
                pkg_data = json.loads(files["package.json"])
                if "name" in pkg_data:
                    project_name = pkg_data["name"].replace("-", " ").title()
                all_deps = {**pkg_data.get("dependencies", {}), **pkg_data.get("devDependencies", {})}
                dependencies = list(all_deps.keys())

                if "pnpm-lock.yaml" in files:
                    package_manager = "pnpm"
                    install_commands = ["pnpm install"]
                    run_commands = ["pnpm dev"]
                elif "yarn.lock" in files:
                    package_manager = "yarn"
                    install_commands = ["yarn install"]
                    run_commands = ["yarn dev"]

                if "next" in all_deps:
                    project_type = "Next.js Web Application"
                    primary_language = "TypeScript / React"
                    run_commands = [f"{package_manager} run dev"]
                elif "react" in all_deps and "vite" in all_deps:
                    project_type = "Vite + React SPA"
                    primary_language = "TypeScript / React"
                elif "express" in all_deps:
                    project_type = "Express Node.js API"
                    primary_language = "JavaScript"
                    run_commands = ["node server.js"]
            except Exception:
                pass

        # 2. Inspect Python manifests
        elif "requirements.txt" in files or "pyproject.toml" in files:
            primary_language = "Python 3"
            package_manager = "pip"
            install_commands = ["python -m venv .venv", "source .venv/bin/activate  # (Windows: .venv\\Scripts\\activate)", "pip install -r requirements.txt"]

            raw_reqs = files.get("requirements.txt", "")
            for line in raw_reqs.splitlines():
                clean_line = line.strip()
                if clean_line and not clean_line.startswith("#"):
                    dep_name = re.split(r"[><=~]", clean_line)[0].strip()
                    dependencies.append(dep_name)

            if "fastapi" in dependencies:
                project_type = "FastAPI Cloud Service"
                run_commands = ["uvicorn main:app --reload"]
            elif "flask" in dependencies:
                project_type = "Flask Web App"
                run_commands = ["flask run"]
            elif "django" in dependencies:
                project_type = "Django Web Application"
                run_commands = ["python manage.py runserver"]
            else:
                project_type = "Python Application"
                run_commands = ["python main.py"]

        # 3. Detect environment variables from .env.example or code scans
        if ".env.example" in files:
            for line in files[".env.example"].splitlines():
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    var_name = line.split("=")[0].strip()
                    if var_name:
                        env_vars.append(var_name)

        # Scan code files for process.env or os.getenv
        for fname, content in files.items():
            if fname.endswith((".js", ".jsx", ".ts", ".tsx")):
                for m in re.finditer(r"process\.env\.([A-Z0-9_]+)", content):
                    var = m.group(1)
                    if var not in env_vars and var not in ("NODE_ENV",):
                        env_vars.append(var)
            elif fname.endswith(".py"):
                for m in re.finditer(r"""os\.(?:getenv|environ\.get)\(['"]([A-Z0-9_]+)['"]\)""", content):
                    var = m.group(1)
                    if var not in env_vars:
                        env_vars.append(var)

        return ProjectAnalysis(
            project_name=project_name,
            project_type=project_type,
            primary_language=primary_language,
            package_manager=package_manager,
            install_commands=install_commands,
            run_commands=run_commands,
            detected_dependencies=dependencies[:15],
            detected_env_vars=env_vars,
            has_docker=has_docker,
        )

    @classmethod
    def generate_readme(
        cls,
        analysis: ProjectAnalysis,
        tagline: str = "Built with passion, AI tools, and clean code.",
    ) -> str:
        """
        Produces a beautiful, neo-minimalist, beginner-friendly Markdown README.
        """
        install_block = "\n".join(analysis.install_commands)
        run_block = "\n".join(analysis.run_commands)

        env_section = ""
        if analysis.detected_env_vars:
            rows = "\n".join([f"| `{v}` | Add your secret key here | Yes |" for v in analysis.detected_env_vars])
            env_section = f"""
## 🔑 Environment Variables Setup

Before starting the app, copy the template and configure your secrets:

```bash
cp .env.example .env
```

| Variable | Description | Required |
| :--- | :--- | :--- |
{rows}

> 💡 **Noob Safety Tip:** Never commit your `.env` file to GitHub! Keep it listed in `.gitignore`.
"""

        docker_section = ""
        if analysis.has_docker:
            docker_section = """
## 🐳 Running with Docker

Prefer containerized workflows? Run everything in one command:

```bash
docker compose up --build
```
"""

        readme_content = f"""# 🚀 {analysis.project_name}

> {tagline}  
> **Type:** `{analysis.project_type}` • **Language:** `{analysis.primary_language}` • **Manager:** `{analysis.package_manager}`

---

## 🌟 What is this project?
Welcome to **{analysis.project_name}**! This repository is organized cleanly so that you can run, tweak, and deploy it without getting stuck in terminal errors or configuration puzzles.

---

## ⚡ Quickstart Guide (Run in 3 Steps)

### 1. Clone the repository
```bash
git clone https://github.com/your-username/{analysis.project_name.lower().replace(" ", "-")}.git
cd {analysis.project_name.lower().replace(" ", "-")}
```

### 2. Install Dependencies
```bash
{install_block}
```

### 3. Launch Development Server
```bash
{run_block}
```

Open your browser at [http://localhost:3000](http://localhost:3000) (or the port shown in your terminal) to see your app live!
{env_section}{docker_section}
---

## 🛠️ Tech Stack & Key Libraries
{"" if not analysis.detected_dependencies else "".join([f"- **`{dep}`**\n" for dep in analysis.detected_dependencies[:10]])}

---

## 🤝 Need Help? (No-Jargon Troubleshooting)

- **Port already in use?** If you see `EADDRINUSE: port 3000`, either close the other terminal running the app or change the port (`PORT=3001 {run_block}`).
- **Missing Module error?** Run `{analysis.install_commands[0]}` again to make sure all dependencies are downloaded.
- **Git Merge Conflict?** Don't panic! Use the **GitHub Noob Toolkit (GNT)** or ask your AI IDE: *"Help me resolve this conflict safely without losing code."*

---

*Generated with ❤️ by [GitHub Noob Toolkit (GNT)](https://github.com/gnt-shield)*
"""
        return readme_content.strip()
