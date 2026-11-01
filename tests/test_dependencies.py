import pytest
from core.dependencies import DepDoctor


def test_python_ast_import_extraction():
    code = """
import os
import sys
from fastapi import FastAPI, Depends
import openai
from .local_module import helper
"""
    imports = DepDoctor.extract_python_imports(code)
    assert "os" in imports
    assert "sys" in imports
    assert "fastapi" in imports
    assert "openai" in imports


def test_audit_python_repository_missing_deps():
    code_files = {
        "main.py": "import os\nimport requests\nfrom PIL import Image\n",
    }
    requirements = "urllib3>=2.0.0\n"

    findings = DepDoctor.audit_python_repository(code_files, requirements_content=requirements)
    pkg_names = [f.package_name for f in findings]

    # 'os' is stdlib, so shouldn't be flagged
    assert "os" not in pkg_names
    # 'requests' is third-party and missing
    assert "requests" in pkg_names
    # 'PIL' maps to 'Pillow' alias
    assert "Pillow" in pkg_names


def test_generate_manifest_patch():
    code_files = {"app.py": "import pydantic\nimport httpx\n"}
    reqs = "fastapi==0.110.0\n"
    findings = DepDoctor.audit_python_repository(code_files, requirements_content=reqs)

    patched = DepDoctor.generate_manifest_patch(findings, reqs, manifest_type="python_requirements")
    assert "fastapi==0.110.0" in patched
    assert "pydantic>=0.1.0" in patched
    assert "httpx>=0.1.0" in patched
