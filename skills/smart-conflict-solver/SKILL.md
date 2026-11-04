---
name: smart-conflict-solver
description: Parses Git merge conflict markers (<<<<<<< HEAD, =======, >>>>>>>) in memory and resolves them safely using Smart Hybrid Merge, Accept Ours, or Accept Theirs strategies.
origin: GNT
---

# ⚔️ Smart Branch Conflict Solver (`smart-conflict-solver`)

Eliminates merge conflict paralysis by analyzing conflicting hunks and producing clean, syntax-valid merged files.

## When to Activate
- When a file contains `<<<<<<<`, `=======`, or `>>>>>>>` conflict markers
- When a Pull Request cannot be merged cleanly due to diverging imports or functions
- Via the FastMCP tool `resolve_conflict`

## Core Capabilities (`core/conflicts.py`)
1. **Smart Hybrid Merge (`hybrid`):** Deduplicates and combines imports and non-overlapping function additions from both `ours` and `theirs`.
2. **Deterministic Fallback Strategies:** Supports `ours` (keep current branch) and `theirs` (accept incoming branch) with plain-English explanations of the trade-offs.

## Usage Example
```python
from core.conflicts import solve_merge_conflict

resolution = solve_merge_conflict(conflicted_code_str, strategy="hybrid")
print(resolution.resolved_content)
```
