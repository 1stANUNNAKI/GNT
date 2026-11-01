import json
import pytest
from core.docgen import DocGen, ProjectAnalysis


def test_analyze_python_fastapi_project():
    files = {
        "requirements.txt": "fastapi>=0.110.0\nuvicorn>=0.28.0\npydantic>=2.0\n",
        ".env.example": "DATABASE_URL=postgres://...\nOPENAI_KEY=sk-...\n",
        "Dockerfile": "FROM python:3.12-slim\n",
    }
    analysis = DocGen.analyze_project_files(files, default_name="AI Backend API")
    assert analysis.primary_language == "Python 3"
    assert analysis.project_type == "FastAPI Cloud Service"
    assert "fastapi" in analysis.detected_dependencies
    assert "DATABASE_URL" in analysis.detected_env_vars
    assert analysis.has_docker is True


def test_analyze_nextjs_project():
    pkg_json = {
        "name": "vibe-dashboard",
        "dependencies": {
            "next": "^14.2.0",
            "react": "^18.2.0",
            "lucide-react": "^0.300.0",
        },
    }
    files = {
        "package.json": json.dumps(pkg_json),
    }
    analysis = DocGen.analyze_project_files(files)
    assert analysis.project_name == "Vibe Dashboard"
    assert "Next.js" in analysis.project_type
    assert analysis.package_manager == "npm"


def test_generate_readme():
    analysis = ProjectAnalysis(
        project_name="Vibe Chat",
        project_type="Next.js Web Application",
        primary_language="TypeScript / React",
        package_manager="npm",
        install_commands=["npm install"],
        run_commands=["npm run dev"],
        detected_dependencies=["next", "react", "lucide-react"],
        detected_env_vars=["NEXT_PUBLIC_API_URL"],
        has_docker=False,
    )
    readme = DocGen.generate_readme(analysis)
    assert "# 🚀 Vibe Chat" in readme
    assert "npm run dev" in readme
    assert "NEXT_PUBLIC_API_URL" in readme
    assert "GitHub Noob Toolkit (GNT)" in readme
