# -*- coding: utf-8 -*-
"""
Automated Git Documentation & Community Health Suite Builder (git-docs-architect).
Usage:
    python build_git_docs.py --repo-dir ./my-repo --project-name "MY-REPO" --owner "1stANUNNAKI"
"""

import argparse
from pathlib import Path

REQUIRED_FILES = [
    "README.md",
    "README_AR.md",
    "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md",
    "LICENSE",
    "SECURITY.md",
    "AGENTS.md",
    "CHANGELOG.md",
    "TROUBLESHOOTING.md",
    ".gitattributes",
]


def audit_repo_docs(repo_dir: Path) -> dict:
    present = []
    missing = []
    for fname in REQUIRED_FILES:
        if (repo_dir / fname).exists():
            present.append(fname)
        else:
            missing.append(fname)
    return {"present": present, "missing": missing, "score": f"{len(present)}/{len(REQUIRED_FILES)}"}


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit or scaffold ECC-grade GitHub documentation files.")
    parser.add_argument("--repo-dir", required=True, help="Target repository directory")
    parser.add_argument("--project-name", default="Project", help="Repository name")
    parser.add_argument("--owner", default="1stANUNNAKI", help="GitHub owner handle")
    args = parser.parse_args()

    repo_path = Path(args.repo_dir).resolve()
    templates_dir = Path(__file__).resolve().parent.parent / "templates"

    if not repo_path.exists():
        raise SystemExit(f"Repository path does not exist: {repo_path}")

    for tmpl_file in templates_dir.glob("*.template*"):
        target_name = tmpl_file.name.replace(".template", "")
        target_path = repo_path / target_name
        if not target_path.exists():
            content = tmpl_file.read_text(encoding="utf-8")
            content = content.replace("{{PROJECT_NAME}}", args.project_name).replace("{{OWNER}}", args.owner)
            target_path.write_text(content, encoding="utf-8")
            print(f"[CREATED] {target_path.name}")

    report = audit_repo_docs(repo_path)
    print(f"[AUDIT] Community Health Score: {report['score']} | Missing: {report['missing']}")


if __name__ == "__main__":
    main()
