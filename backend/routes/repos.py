"""
Repository Management and On-Demand Scanning Routes.
"""

from __future__ import annotations
import json
from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.secrets import SecretShield, Severity
from core.conflicts import ConflictSolver
from core.dependencies import DepDoctor
from core.health_score import VibeHealthScore
from ..database import get_db
from ..models import Repository, ScanResult, User
from ..schemas import OnDemandScanRequest, RepoCreate, RepoRead
from .auth import get_current_user


router = APIRouter(prefix="/api/repos", tags=["Repositories"])


@router.get("", response_model=List[RepoRead])
async def list_repositories(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Lists all repositories connected to the user's account."""
    query = select(Repository).where(Repository.user_id == user.id).order_by(desc(Repository.created_at))
    res = await db.execute(query)
    repos = res.scalars().all()

    # If empty, populate with a starter repository for immediate exploration
    if not repos:
        starter = Repository(
            user_id=user.id,
            github_repo_id=1010101,
            full_name=f"{user.username}/my-first-vibe-app",
            is_private=False,
            default_branch="main",
            vibe_health_score=95,
            last_scanned_at=datetime.utcnow(),
        )
        db.add(starter)
        await db.commit()
        await db.refresh(starter)
        return [starter]

    return repos


@router.post("", response_model=RepoRead, status_code=status.HTTP_201_CREATED)
async def add_repository(
    repo_in: RepoCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Connects a new repository to GNT."""
    repo = Repository(
        user_id=user.id,
        github_repo_id=repo_in.github_repo_id,
        full_name=repo_in.full_name,
        is_private=repo_in.is_private,
        default_branch=repo_in.default_branch,
        vibe_health_score=100,
        last_scanned_at=datetime.utcnow(),
    )
    db.add(repo)
    await db.commit()
    await db.refresh(repo)
    return repo


@router.get("/{repo_id}", response_model=RepoRead)
async def get_repository(
    repo_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Fetches details for a single repository."""
    query = select(Repository).where(Repository.id == repo_id, Repository.user_id == user.id)
    res = await db.execute(query)
    repo = res.scalar_one_or_none()
    if not repo:
        raise HTTPException(status_code=404, detail="Repository not found.")
    return repo


@router.post("/{repo_id}/scan")
async def trigger_on_demand_scan(
    repo_id: str,
    scan_req: OnDemandScanRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Triggers an in-memory safety and quality audit across provided file contents.
    Runs SecretShield, DepDoctor, and ConflictSolver.
    """
    query = select(Repository).where(Repository.id == repo_id, Repository.user_id == user.id)
    res = await db.execute(query)
    repo = res.scalar_one_or_none()
    if not repo:
        raise HTTPException(status_code=404, detail="Repository not found.")

    shield = SecretShield()
    all_findings = []
    active_conflicts = 0

    # 1. Scan files for secrets and merge conflicts
    for filepath, content in scan_req.file_contents.items():
        findings = shield.scan_text(content, file_path=filepath)
        all_findings.extend(findings)

        conflict_res = ConflictSolver.analyze_file_content(content)
        if conflict_res.has_conflicts:
            active_conflicts += conflict_res.total_conflicts

    # 2. Check dependencies (Python / Node)
    reqs_content = scan_req.file_contents.get("requirements.txt", "")
    py_files = {k: v for k, v in scan_req.file_contents.items() if k.endswith(".py")}
    missing_deps = DepDoctor.audit_python_repository(py_files, requirements_content=reqs_content)

    # 3. Calculate Vibe Health Score
    critical_leaks = sum(1 for f in all_findings if f.severity == Severity.CRITICAL)
    high_leaks = sum(1 for f in all_findings if f.severity == Severity.HIGH)
    forbidden_files = sum(1 for f in all_findings if f.rule_id == "FORBIDDEN_FILE_TRACKED")
    has_readme = any("readme" in k.lower() for k in scan_req.file_contents.keys())

    audit = VibeHealthScore.calculate(
        critical_secrets_count=critical_leaks,
        high_secrets_count=high_leaks,
        forbidden_files_count=forbidden_files,
        has_readme=has_readme,
        active_conflicts_count=active_conflicts,
        missing_dependencies_count=len(missing_deps),
    )

    # Update repo health score
    repo.vibe_health_score = audit.score
    repo.last_scanned_at = datetime.utcnow()

    # Record scan log
    scan_log = ScanResult(
        repository_id=repo.id,
        score=audit.score,
        critical_leaks=critical_leaks,
        high_leaks=high_leaks,
        conflicts_count=active_conflicts,
        missing_deps_count=len(missing_deps),
        details_json=json.dumps(
            {
                "audit": audit.to_dict(),
                "findings": [f.to_dict() for f in all_findings],
                "missing_deps": [m.to_dict() for m in missing_deps],
            }
        ),
    )
    db.add(scan_log)
    await db.commit()
    await db.refresh(scan_log)

    return {
        "status": "success",
        "score": audit.score,
        "vibe_status": audit.status.value,
        "encouraging_message": audit.encouraging_message,
        "penalties": [p.to_dict() for p in audit.penalties],
        "findings": [f.to_dict() for f in all_findings],
        "missing_dependencies": [m.to_dict() for m in missing_deps],
    }
