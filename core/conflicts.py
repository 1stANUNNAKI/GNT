"""
Branch Conflict Solver Module.
Analyzes merge conflict markers (<<<<<<< HEAD, =======, >>>>>>>) in-memory,
breaks down what each branch changed, explains it in human terms,
and generates safe conflict-free patches.
"""

from __future__ import annotations
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Tuple


class ConflictResolutionStrategy(str, Enum):
    ACCEPT_OURS = "ours"
    ACCEPT_THEIRS = "theirs"
    SMART_HYBRID = "smart_hybrid"  # Combines both without duplicates (ideal for imports & lists)


@dataclass
class ConflictBlock:
    block_index: int
    start_line: int
    end_line: int
    ours_label: str
    ours_content: str
    theirs_label: str
    theirs_content: str
    friendly_explanation: str
    recommended_strategy: ConflictResolutionStrategy

    def to_dict(self) -> dict:
        return {
            "block_index": self.block_index,
            "lines": f"{self.start_line}-{self.end_line}",
            "ours_label": self.ours_label,
            "ours_content": self.ours_content,
            "theirs_label": self.theirs_label,
            "theirs_content": self.theirs_content,
            "friendly_explanation": self.friendly_explanation,
            "recommended_strategy": self.recommended_strategy.value,
        }


@dataclass
class ConflictResolution:
    has_conflicts: bool
    total_conflicts: int
    blocks: List[ConflictBlock] = field(default_factory=list)
    resolved_text: str = ""
    summary_message: str = ""


class ConflictSolver:
    """
    In-memory parser and resolver for Git merge conflicts.
    Takes away the fear of '<<<<<<< HEAD' git markers.
    """

    CONFLICT_PATTERN = re.compile(
        r"<{7}\s*(?P<ours_label>[^\r\n]*)\r?\n(?P<ours_content>[\s\S]*?)={7}\r?\n(?P<theirs_content>[\s\S]*?)>{7}\s*(?P<theirs_label>[^\r\n]*)\r?\n"
    )

    @classmethod
    def analyze_file_content(cls, content: str) -> ConflictResolution:
        """
        Parses all conflict markers in a string.
        """
        matches = list(cls.CONFLICT_PATTERN.finditer(content))
        if not matches:
            return ConflictResolution(
                has_conflicts=False,
                total_conflicts=0,
                blocks=[],
                resolved_text=content,
                summary_message="Awesome! No merge conflicts detected in this file.",
            )

        blocks: List[ConflictBlock] = []
        for idx, match in enumerate(matches, start=1):
            # Calculate rough line numbers
            start_pos = match.start()
            start_line = content[:start_pos].count("\n") + 1
            end_line = start_line + match.group(0).count("\n")

            ours_lbl = match.group("ours_label").strip() or "HEAD (Your current changes)"
            theirs_lbl = match.group("theirs_label").strip() or "Incoming changes"
            ours_code = match.group("ours_content")
            theirs_code = match.group("theirs_content")

            # Determine conflict nature
            strategy, explanation = cls._evaluate_block(ours_code, theirs_code)

            blocks.append(
                ConflictBlock(
                    block_index=idx,
                    start_line=start_line,
                    end_line=end_line,
                    ours_label=ours_lbl,
                    ours_content=ours_code,
                    theirs_label=theirs_lbl,
                    theirs_content=theirs_code,
                    friendly_explanation=explanation,
                    recommended_strategy=strategy,
                )
            )

        summary = (
            f"Found {len(blocks)} conflict block(s). Don't panic! "
            f"This just means both you and another branch edited the same lines."
        )

        # Generate default resolved text using recommended smart strategies
        resolved_text = cls.resolve_conflicts(content, default_strategy=ConflictResolutionStrategy.SMART_HYBRID)

        return ConflictResolution(
            has_conflicts=True,
            total_conflicts=len(blocks),
            blocks=blocks,
            resolved_text=resolved_text,
            summary_message=summary,
        )

    @classmethod
    def resolve_conflicts(
        cls,
        content: str,
        default_strategy: ConflictResolutionStrategy = ConflictResolutionStrategy.SMART_HYBRID,
    ) -> str:
        """
        Replaces conflict blocks in content with chosen resolved output.
        """
        def replacer(match: re.Match) -> str:
            ours = match.group("ours_content")
            theirs = match.group("theirs_content")
            strategy, _ = cls._evaluate_block(ours, theirs)
            chosen_strategy = strategy if default_strategy == ConflictResolutionStrategy.SMART_HYBRID else default_strategy

            if chosen_strategy == ConflictResolutionStrategy.ACCEPT_OURS:
                return ours
            elif chosen_strategy == ConflictResolutionStrategy.ACCEPT_THEIRS:
                return theirs
            else:
                return cls._smart_merge_text(ours, theirs)

        return cls.CONFLICT_PATTERN.sub(replacer, content)

    @classmethod
    def _evaluate_block(cls, ours: str, theirs: str) -> Tuple[ConflictResolutionStrategy, str]:
        """
        Evaluates the semantic nature of the two conflicting versions.
        """
        ours_lines = [l.strip() for l in ours.splitlines() if l.strip()]
        theirs_lines = [l.strip() for l in theirs.splitlines() if l.strip()]

        # Case 1: Both sides are just adding imports or requires
        if (
            all(l.startswith(("import ", "from ", "const ", "require(")) for l in ours_lines)
            and all(l.startswith(("import ", "from ", "const ", "require(")) for l in theirs_lines)
        ):
            return (
                ConflictResolutionStrategy.SMART_HYBRID,
                "Both branches added library imports. We can safely merge both lists without duplicates.",
            )

        # Case 2: One side is completely empty (deletion vs retention)
        if not ours_lines and theirs_lines:
            return (
                ConflictResolutionStrategy.ACCEPT_THEIRS,
                "Your branch deleted these lines while the incoming branch kept them. "
                "Recommendation: Keep the incoming code unless you intentionally wanted it deleted.",
            )
        if ours_lines and not theirs_lines:
            return (
                ConflictResolutionStrategy.ACCEPT_OURS,
                "The incoming branch deleted these lines while you added or kept them. "
                "Recommendation: Keep your changes.",
            )

        # Case 3: Both added distinct functions or class methods
        ours_is_fn = any(l.startswith(("def ", "function ", "export const ", "class ")) for l in ours_lines)
        theirs_is_fn = any(l.startswith(("def ", "function ", "export const ", "class ")) for l in theirs_lines)
        if ours_is_fn and theirs_is_fn:
            return (
                ConflictResolutionStrategy.SMART_HYBRID,
                "Both branches created brand new functions. We can keep both functions side by side!",
            )

        # Case 4: General divergence
        return (
            ConflictResolutionStrategy.ACCEPT_OURS,
            "Both branches modified the exact same logic. Defaulting to keep your local branch work (Ours).",
        )

    @staticmethod
    def _smart_merge_text(ours: str, theirs: str) -> str:
        """
        Deduplicates lines and combines them cleanly.
        """
        seen = set()
        merged_lines = []

        for line in ours.splitlines():
            s = line.strip()
            if s and s not in seen:
                seen.add(s)
                merged_lines.append(line)
            elif not s:
                merged_lines.append(line)

        for line in theirs.splitlines():
            s = line.strip()
            if s and s not in seen:
                seen.add(s)
                merged_lines.append(line)
            elif not s and merged_lines and merged_lines[-1] != "":
                merged_lines.append(line)

        return "\n".join(merged_lines) + "\n"
