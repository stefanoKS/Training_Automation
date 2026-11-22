"""Build read-only Markdown-cell notebooks from the Day 7-9 lesson manuscripts.

Run from any directory:
    python AI_Vision_Training\\day07_09_support\\scripts\\build_day07_09_notebooks.py

The manuscripts are the single source of instructional content. Each run is
deterministic and records the source SHA-256 in the notebook metadata so that a
stale notebook can be detected before PDF export or tests.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NOTEBOOKS = ROOT / "notebooks"

DAYS = {
    "Day07_Machine_Fundamentals": (
        "Day07_01_Mechanical_Fundamentals",
        "Day07_02_Sensors_and_Signals",
        "Day07_03_Actuators_and_Machine",
    ),
    "Day08_PLC_Control": (
        "Day08_01_PLC_Fundamentals",
        "Day08_02_Ladder_Basics",
        "Day08_03_Sequence_Control",
    ),
    "Day09_System_Integration": (
        "Day09_01_Vision_Hardware",
        "Day09_02_PC_AI_Processing",
        "Day09_03_Complete_Integration",
    ),
}


def sections_of(text: str) -> list[str]:
    """Split a manuscript into cells at level-2 headings (``## ``)."""
    sections: list[list[str]] = []
    for line in text.splitlines(keepends=True):
        if line.startswith("## ") or not sections:
            sections.append([])
        sections[-1].append(line)
    return ["".join(section) for section in sections]


def build_lesson(directory: Path, name: str) -> Path:
    manuscript = directory / f"{name}.md"
    data = manuscript.read_bytes()
    text = data.decode("utf-8")
    sections = sections_of(text)
    notebook = {
        "cells": [
            {
                "cell_type": "markdown",
                "id": f"{name.lower()[:20]}-{index:02}",
                "metadata": {},
                "source": section,
            }
            for index, section in enumerate(sections)
        ],
        "metadata": {
            "day07_09_source_sha256": hashlib.sha256(data).hexdigest(),
            "day07_09_source": f"{name}.md",
            "kernelspec": {"name": "python3", "display_name": "Python 3"},
            "language_info": {"name": "python"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    output = directory / f"{name}.ipynb"
    output.write_text(json.dumps(notebook, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return output


def build() -> None:
    total = 0
    for folder, lessons in DAYS.items():
        directory = NOTEBOOKS / folder
        for name in lessons:
            output = build_lesson(directory, name)
            cells = json.loads(output.read_text(encoding="utf-8"))["cells"]
            print(f"Built {output.relative_to(ROOT)}: {len(cells)} Markdown cells")
            total += 1
    print(f"Built {total} notebooks")


if __name__ == "__main__":
    build()
