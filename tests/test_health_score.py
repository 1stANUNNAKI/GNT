import pytest
from core.health_score import VibeHealthScore, VibeStatus


def test_perfect_health_score():
    res = VibeHealthScore.calculate(
        critical_secrets_count=0,
        high_secrets_count=0,
        forbidden_files_count=0,
        has_readme=True,
        active_conflicts_count=0,
        missing_dependencies_count=0,
    )
    assert res.score == 100
    assert res.status == VibeStatus.CERTIFIED
    assert len(res.penalties) == 0


def test_health_score_with_leaked_secrets():
    res = VibeHealthScore.calculate(
        critical_secrets_count=2,
        high_secrets_count=0,
        forbidden_files_count=1,
        has_readme=True,
        active_conflicts_count=0,
        missing_dependencies_count=0,
    )
    assert res.score < 50
    assert res.status == VibeStatus.CRITICAL
    assert len(res.penalties) == 2
