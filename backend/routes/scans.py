"""
Scan Results and History Endpoints.
"""

from __future__ import annotations
import json
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..models import Repository, ScanResult, User
from ..schemas import ScanResultRead
from .auth import get_current_user


router = APIRouter(prefix="/api/scans", tags=["Scans"])


@router.get("/repo/{repo_id}", response_model=List[ScanResultRead])
async def get_repo_scans(
    repo_id: str,
    limit: int = 10,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Fetches scan history for a given repository."""
    # Verify ownership
    res = await db.execute(select(Repository).where(Repository.id == repo_id, Repository.user_id == user.id))
    repo = res.scalar_one_or_none()
    if not repo:
        raise HTTPException(status_code=404, detail="Repository not found.")

    query = select(ScanResult).where(ScanResult.repository_id == repo_id).order_by(desc(ScanResult.created_at)).limit(limit)
    res_scans = await db.execute(query)
    scans = res_scans.scalars().all()

    output = []
    for s in scans:
        try:
            parsed = json.loads(s.details_json)
        except Exception:
            parsed = {}
        output.append(
            ScanResultRead(
                id=s.id,
                repository_id=s.repository_id,
                commit_sha=s.commit_sha,
                pull_request_number=s.pull_request_number,
                score=s.score,
                critical_leaks=s.critical_leaks,
                high_leaks=s.high_leaks,
                conflicts_count=s.conflicts_count,
                missing_deps_count=s.missing_deps_count,
                details=parsed,
                created_at=s.created_at,
            )
        )
    return output
