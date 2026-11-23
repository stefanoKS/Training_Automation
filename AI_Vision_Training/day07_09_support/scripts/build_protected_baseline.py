"""Build the protected-file baseline for Days 1-6 and the source PDF.

Run from any directory:
    python AI_Vision_Training\\day07_09_support\\scripts\\build_protected_baseline.py

The baseline stores `git hash-object` values.  It is meaningful both before and
after a commit: it checks file content, not the absence of working-tree changes.
Only Days 1-6 materials and the immutable source PDF are protected; the Day 7-9
replacement is deliberately outside the baseline.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REPO = ROOT.parent
OUTPUT = ROOT / "day07_09_support" / "reference_data" / "protected_baseline_hashes.txt"
PREFIXES = (
    "AI_Vision_Training/notebooks/00_Setup/",
    "AI_Vision_Training/notebooks/Day01_",
    "AI_Vision_Training/notebooks/Day02_",
    "AI_Vision_Training/notebooks/Day03_",
    "AI_Vision_Training/notebooks/Day04_",
    "AI_Vision_Training/notebooks/Day05_",
    "AI_Vision_Training/notebooks/Day06_",
    "AI_Vision_Training/day06_support/",
    "AI_Vision_Training/assets/",
    "AI_Vision_Training/docs/instructor/day01_",
    "AI_Vision_Training/docs/instructor/day02_",
    "AI_Vision_Training/docs/instructor/day03_",
    "AI_Vision_Training/docs/instructor/day04_",
    "AI_Vision_Training/docs/instructor/day05_",
    "AI_Vision_Training/docs/instructor/day06_",
    "AI_Vision_Training/docs/pdf/Day01_",
    "AI_Vision_Training/docs/pdf/Day02_",
    "AI_Vision_Training/docs/pdf/Day03_",
    "AI_Vision_Training/docs/pdf/Day04_",
    "AI_Vision_Training/docs/pdf/Day05_",
    "AI_Vision_Training/docs/pdf/Day06_",
    "AI_Vision_Training/docs/pdf/Week1_",
    "AI_Vision_Training/docs/pdf/Course_Syllabus_",
    "AI_Vision_Training/docs/pdf/Installation_Guide_",
    "AI_Vision_Training/docs/pdf/Repository_Guide_",
    "AI_Vision_Training/docs/pdf/Setup_",
    "AI_Vision_Training/docs/reference/",
    "AI_Vision_Training/docs/troubleshooting/",
    "AI_Vision_Training/requirements/",
    "AI_Vision_Training/COURSE_SYLLABUS.md",
    "AI_Vision_Training/COURSE_SYLLABUS_DAY06.md",
    "AI_Vision_Training/start_training.cmd",
)
EXCLUDE = (
    "/diagrams/day07/",
    "/diagrams/day08/",
    "/diagrams/day09/",
    "docs/pdf/_pages/Day07",
    "docs/pdf/_pages/Day08",
    "docs/pdf/_pages/Day09",
)


def main() -> int:
    tracked = subprocess.check_output(["git", "ls-files"], cwd=REPO, text=True).splitlines()
    selected = []
    for relative in tracked:
        if not relative.startswith("AI_Vision_Training/"):
            continue
        if any(token in relative for token in EXCLUDE):
            continue
        if not relative.startswith(PREFIXES):
            continue
        if not (REPO / relative).is_file():
            continue
        selected.append(relative)
    selected.sort()
    lines = []
    for relative in selected:
        digest = subprocess.check_output(["git", "hash-object", str(REPO / relative)], cwd=REPO, text=True).strip()
        lines.append(f"{digest}  {relative}")
    OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {len(lines)} protected entries to {OUTPUT.relative_to(ROOT)}")
    if len(lines) < 300:
        print("warning: fewer than 300 protected entries", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
