"""Build the nine Day 7-9 Jupyter notebooks from canonical bilingual manuscripts.

Run from any directory:
    python AI_Vision_Training\\day07_09_support\\scripts\\build_day07_09_notebooks.py
    python ...\\build_day07_09_notebooks.py --check

Architecture
------------
* ``lesson_manifest.json`` defines day order, lesson order, time slot, source
  PDF pages and the diagrams owned by each lesson.
* Each ``DayNN_MM_Title.md`` manuscript is the canonical instructional text.
* A fenced block opened with ```` ```python exec ```` becomes an executable
  code cell.  Every other fenced block stays inside a Markdown cell, so
  illustrative pseudo-code is never executed by accident.
* A notebook stores a combined fingerprint of every input that determines its
  content (manifest, manuscript, shared model module, referenced SVG figures
  and this generator).  ``--check`` detects a stale notebook without executing
  anything.

The build is deterministic: running it twice produces identical bytes.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SUPPORT = ROOT / "day07_09_support"
NOTEBOOKS = ROOT / "notebooks"
MANIFEST_PATH = SUPPORT / "lesson_manifest.json"
MODEL_PATH = SUPPORT / "examples" / "automation_models.py"
GENERATOR_PATH = Path(__file__).resolve()
FINGERPRINT_SCHEMA = "day07_09_notebook_v3"
EXEC_FENCE = re.compile(r"^```python\s+exec(?:\s+id=\"(?P<id>[^\"]+)\")?\s*$")
IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)\s]+)\)")


@dataclass(frozen=True)
class LessonSpec:
    day_id: str
    folder: str
    name: str
    order: int
    duration_min: int
    title_ja: str
    title_en: str
    pdf_pages: str
    diagrams: tuple[str, ...]

    @property
    def manuscript(self) -> Path:
        return NOTEBOOKS / self.folder / f"{self.name}.md"

    @property
    def notebook(self) -> Path:
        return NOTEBOOKS / self.folder / f"{self.name}.ipynb"


def load_manifest(path: Path = MANIFEST_PATH) -> dict:
    if not path.is_file():
        raise FileNotFoundError(f"missing manifest: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_version") != 2:
        raise ValueError("unsupported lesson manifest schema")
    return data


def lesson_specs(manifest: dict | None = None) -> list[LessonSpec]:
    manifest = manifest or load_manifest()
    specs: list[LessonSpec] = []
    for day in manifest["days"]:
        for lesson in day["lessons"]:
            specs.append(
                LessonSpec(
                    day_id=day["id"],
                    folder=day["folder"],
                    name=lesson["name"],
                    order=int(lesson["order"]),
                    duration_min=int(lesson["duration_min"]),
                    title_ja=lesson["title_ja"],
                    title_en=lesson["title_en"],
                    pdf_pages=str(lesson.get("pdf_pages", "")),
                    diagrams=tuple(lesson.get("diagrams", ())),
                )
            )
    if len(specs) != 9:
        raise ValueError(f"expected nine lessons, manifest defines {len(specs)}")
    for spec in specs:
        if spec.manuscript.parent != spec.notebook.parent:
            raise ValueError("manuscript/notebook folder mismatch")
    return specs


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def dependency_paths(spec: LessonSpec, text: str) -> list[Path]:
    deps = [MANIFEST_PATH, spec.manuscript, MODEL_PATH, GENERATOR_PATH]
    for link in IMAGE_RE.findall(text):
        if link.startswith(("http://", "https://", "data:")):
            raise ValueError(f"{spec.name}: remote images are not allowed: {link}")
        target = (spec.notebook.parent / link).resolve()
        if ROOT not in target.parents:
            raise ValueError(f"{spec.name}: image escapes the repository: {link}")
        if not target.is_file():
            raise FileNotFoundError(f"{spec.name}: missing figure {link}")
        deps.append(target)
    seen: set[Path] = set()
    unique = []
    for path in deps:
        resolved = path.resolve()
        if resolved not in seen:
            seen.add(resolved)
            unique.append(resolved)
    return unique


def fingerprint(spec: LessonSpec, text: str) -> tuple[str, list[dict]]:
    deps = dependency_paths(spec, text)
    records = []
    digest = hashlib.sha256(FINGERPRINT_SCHEMA.encode("utf-8"))
    for path in sorted(deps, key=lambda item: item.relative_to(ROOT).as_posix()):
        relative = path.relative_to(ROOT).as_posix()
        file_hash = sha256_file(path)
        records.append({"path": relative, "sha256": file_hash})
        digest.update(f"{relative}\0{file_hash}\n".encode("utf-8"))
    return digest.hexdigest(), records


def parse_manuscript(text: str) -> list[dict]:
    """Split a manuscript into Markdown and executable Python cells."""
    lines = text.splitlines(keepends=True)
    cells: list[dict] = []
    markdown_buffer: list[str] = []
    index = 0

    def flush_markdown() -> None:
        nonlocal markdown_buffer
        source = "".join(markdown_buffer).strip("\n")
        if source.strip():
            cells.append({"cell_type": "markdown", "source": source + "\n"})
        markdown_buffer = []

    while index < len(lines):
        line = lines[index]
        opening = EXEC_FENCE.match(line.strip())
        if opening:
            flush_markdown()
            index += 1
            code: list[str] = []
            while index < len(lines) and not lines[index].strip().startswith("```"):
                code.append(lines[index])
                index += 1
            if index >= len(lines):
                raise ValueError("unterminated `python exec` block")
            index += 1  # closing fence
            source = "".join(code).rstrip("\n") + "\n"
            if not source.strip():
                raise ValueError("empty `python exec` block")
            cells.append(
                {
                    "cell_type": "code",
                    "source": source,
                    "exec_id": opening.group("id") or f"code-{len(cells) + 1:02d}",
                }
            )
            continue

        if line.startswith("```"):
            # Keep illustrative fenced blocks, including their fences, as Markdown.
            fence = line.strip()
            markdown_buffer.append(line)
            index += 1
            while index < len(lines):
                markdown_buffer.append(lines[index])
                if lines[index].strip().startswith("```") and len(lines[index].strip()) >= 3:
                    index += 1
                    break
                index += 1
            continue

        markdown_buffer.append(line)
        index += 1

    flush_markdown()
    return cells


def build_notebook(spec: LessonSpec, manifest: dict) -> tuple[dict, list[dict]]:
    if not spec.manuscript.is_file():
        raise FileNotFoundError(f"missing manuscript: {spec.manuscript}")
    text = spec.manuscript.read_text(encoding="utf-8")
    if not re.search(r"[\u3040-\u30ff\u4e00-\u9fff]", text):
        raise ValueError(f"{spec.name}: Japanese content missing")
    if not re.search(r"\b(?:the|and|with|for|is|are)\b", text, re.I):
        raise ValueError(f"{spec.name}: English content missing")
    if "TODO" in text or "TBD" in text or "PLACEHOLDER" in text.upper():
        raise ValueError(f"{spec.name}: placeholder text is not allowed")

    raw_cells = parse_manuscript(text)
    cells = []
    code_number = 0
    for order, raw in enumerate(raw_cells):
        cell_id = f"{spec.name.lower().replace('_', '-')[:34]}-{order:02d}"
        if raw["cell_type"] == "code":
            code_number += 1
            cells.append(
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "id": cell_id,
                    "metadata": {"tags": ["executable"], "day07_09_exercise": raw["exec_id"]},
                    "outputs": [],
                    "source": raw["source"],
                }
            )
        else:
            cells.append(
                {
                    "cell_type": "markdown",
                    "id": cell_id,
                    "metadata": {},
                    "source": raw["source"],
                }
            )
    if code_number < 3:
        raise ValueError(f"{spec.name}: requires at least 3 executable cells, found {code_number}")

    combined, deps = fingerprint(spec, text)
    notebook = {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.11"},
            "day07_09_generated": True,
            "day07_09_generator": FINGERPRINT_SCHEMA,
            "day07_09_source": f"{spec.name}.md",
            "day07_09_source_sha256": combined,
            "day07_09_manuscript_sha256": sha256_file(spec.manuscript),
            "day07_09_dependencies": deps,
            "day07_09_day": spec.day_id,
            "day07_09_title_ja": spec.title_ja,
            "day07_09_title_en": spec.title_en,
            "day07_09_duration_min": spec.duration_min,
            "day07_09_pdf_pages": spec.pdf_pages,
            "day07_09_diagrams": list(spec.diagrams),
            "day07_09_manifest_schema": manifest["schema_version"],
            "day07_09_executable_cells": code_number,
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    return notebook, deps


def render_notebook(notebook: dict) -> str:
    return json.dumps(notebook, ensure_ascii=False, indent=1) + "\n"


def build(write: bool = True) -> list[Path]:
    manifest = load_manifest()
    outputs = []
    for spec in lesson_specs(manifest):
        notebook, _ = build_notebook(spec, manifest)
        spec.notebook.parent.mkdir(parents=True, exist_ok=True)
        rendered = render_notebook(notebook)
        if write:
            spec.notebook.write_text(rendered, encoding="utf-8")
        markdown_cells = sum(1 for cell in notebook["cells"] if cell["cell_type"] == "markdown")
        outputs.append(spec.notebook)
        print(
            f"{'Built' if write else 'Checked'} {spec.notebook.relative_to(ROOT)}: "
            f"{len(notebook['cells'])} cells "
            f"({markdown_cells} Markdown, {notebook['metadata']['day07_09_executable_cells']} executable)"
        )
    return outputs


def stale_notebooks() -> list[str]:
    manifest = load_manifest()
    stale = []
    for spec in lesson_specs(manifest):
        if not spec.notebook.is_file():
            stale.append(f"{spec.notebook.name}: missing")
            continue
        stored = json.loads(spec.notebook.read_text(encoding="utf-8"))
        combined, _ = fingerprint(spec, spec.manuscript.read_text(encoding="utf-8"))
        if stored.get("metadata", {}).get("day07_09_source_sha256") != combined:
            stale.append(f"{spec.notebook.name}: source fingerprint changed")
    return stale


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="report stale notebooks without writing")
    args = parser.parse_args()
    if args.check:
        stale = stale_notebooks()
        if stale:
            print("STALE:")
            for item in stale:
                print(f"  - {item}")
            return 1
        print("All nine notebooks match their canonical sources.")
        return 0
    build(write=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
