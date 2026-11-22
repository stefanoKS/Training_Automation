"""Build read-only Markdown-cell notebooks from the Day 6 lesson manuscripts."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from render_pricing import SOURCES, load_snapshot, render_lesson_table, render_source_document

ROOT = Path(__file__).resolve().parents[2]
LESSON_DIR = ROOT / "notebooks" / "Day06_LLM_Agents"
LESSONS = (
    "Day06_01_LLM_Fundamentals",
    "Day06_02_Agents_and_Harness",
    "Day06_03_Idea_to_Specification",
    "Day06_04_Prompting_and_Execution",
    "Day06_05_Verification_and_Cost",
)


def build() -> None:
    snapshot = load_snapshot()
    SOURCES.write_text(render_source_document(snapshot), encoding="utf-8")
    for name in LESSONS:
        manuscript = LESSON_DIR / f"{name}.md"
        data = manuscript.read_bytes()
        text = data.decode("utf-8").replace("<!-- DAY06_PRICE_TABLE -->", render_lesson_table(snapshot))
        text = text.replace(
            "<!-- DAY06_PROMPT_LIBRARY -->",
            (ROOT / "day06_support" / "examples" / "example_agent_prompts_ja_en.md").read_text(
                encoding="utf-8"
            ).replace("# コピーして調整する指示集 / Adaptable bilingual prompt library", ""),
        )
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
        output = LESSON_DIR / f"{name}.ipynb"
        output.write_text(
            json.dumps(notebook, ensure_ascii=False, indent=1) + "\n",
            encoding="utf-8",
        )
        print(f"Built {output.name}: {len(sections)} Markdown cells")


if __name__ == "__main__":
    build()
