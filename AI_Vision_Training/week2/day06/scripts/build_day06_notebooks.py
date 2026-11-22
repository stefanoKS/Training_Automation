"""Build read-only Markdown-cell notebooks from the Day 6 lesson manuscripts."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LESSONS = (
    "Day06_01_LLM_Agent_Harness",
    "Day06_02_Ideas_and_Requirements",
    "Day06_03_Prompting_and_Agents",
    "Day06_04_Testing_and_Handover",
)


def build() -> None:
    for name in LESSONS:
        manuscript = ROOT / "lessons" / f"{name}.md"
        data = manuscript.read_bytes()
        text = data.decode("utf-8")
        # A heading starts a new notebook cell; Markdown remains the sole lesson manuscript.
        sections = []
        for line in text.splitlines(keepends=True):
            if line.startswith("## ") and sections:
                sections.append([])
            if not sections:
                sections.append([])
            sections[-1].append(line)
        notebook = {
            "cells": [
                {"cell_type": "markdown", "id": f"{name.lower()[:16]}-{index:02}",
                 "metadata": {}, "source": section}
                for index, section in enumerate(sections)
            ],
            "metadata": {
                "day06_source_sha256": hashlib.sha256(data).hexdigest(),
                "day06_source": f"{name}.md",
            },
            "nbformat": 4,
            "nbformat_minor": 5,
        }
        output = ROOT / "lessons" / f"{name}.ipynb"
        output.write_text(
            json.dumps(notebook, ensure_ascii=False, indent=1) + "\n",
            encoding="utf-8",
        )
        print(f"Built {output.name}: {len(sections)} Markdown cells")


if __name__ == "__main__":
    build()
