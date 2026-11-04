---
name: vibe-health-scorer
description: Computes a comprehensive 0-100 Repository Vibe Health Score with letter grades (A+ to F) across security leaks, documentation completeness, dependency hygiene, and merge readiness.
origin: GNT
---

# 📊 Vibe Health Score Engine (`vibe-health-scorer`)

Evaluates overall repository readiness on a 0–100 scale and provides actionable recommendations to reach `100/100 (Grade A+)`.

## When to Activate
- During repository audits, PR gates, or dashboard health checks
- Via the FastMCP tool `calculate_vibe_score`

## Scoring Formula (`core/health_score.py`)
- Starts at **100 points**:
  - `-40 pts` per critical secret leak (capped at `-70`)
  - `-15 pts` if `README.md` is missing or under-documented
  - `-10 pts` per undeclared dependency (capped at `-30`)
  - `-20 pts` if unresolved merge conflict markers exist

## Usage Example
```python
from core.health_score import compute_vibe_health_score

score = compute_vibe_health_score(secret_count=0, has_readme=True, missing_deps_count=0, has_conflicts=False)
print(f"Score: {score.score}/100 ({score.grade}) - {score.status_label}")
```
