import pytest
from core.conflicts import ConflictSolver, ConflictResolutionStrategy


def test_conflict_solver_no_conflicts():
    clean_code = "print('Hello, clean world!')\n"
    res = ConflictSolver.analyze_file_content(clean_code)
    assert res.has_conflicts is False
    assert res.total_conflicts == 0
    assert res.resolved_text == clean_code


def test_conflict_solver_import_merging():
    conflict_code = """import os
<<<<<<< HEAD
import requests
=======
import httpx
>>>>>>> feature/async-client
print('Done')
"""
    res = ConflictSolver.analyze_file_content(conflict_code)
    assert res.has_conflicts is True
    assert res.total_conflicts == 1
    assert res.blocks[0].recommended_strategy == ConflictResolutionStrategy.SMART_HYBRID

    # Test smart resolution
    resolved = ConflictSolver.resolve_conflicts(conflict_code, default_strategy=ConflictResolutionStrategy.SMART_HYBRID)
    assert "<<<<<<<" not in resolved
    assert "import requests" in resolved
    assert "import httpx" in resolved


def test_conflict_solver_accept_ours():
    conflict_code = """
<<<<<<< HEAD
const PORT = 3000;
=======
const PORT = 8080;
>>>>>>> main
"""
    resolved = ConflictSolver.resolve_conflicts(conflict_code, default_strategy=ConflictResolutionStrategy.ACCEPT_OURS)
    assert "PORT = 3000" in resolved
    assert "PORT = 8080" not in resolved
