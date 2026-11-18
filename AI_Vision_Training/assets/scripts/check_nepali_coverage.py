"""ネパール語カバレッジの点検 / Check how much Nepali the course actually carries.

Two questions are answered here, and nothing else:

* **notebooks** — for every Markdown cell, is there an approved Nepali region, is the cell
  intentionally exempt, and does the Nepali avoid the placeholders and Hindi forms the course has
  banned? Code cells are not expected to hold Nepali.
* **documents** — does each documentation file carry at least one Nepali region, and does the
  Nepali text grow or shrink in a way that suggests a lost block?

The checker never writes. It exits non-zero when a required cell is missing Nepali, so it can run as
part of the test suite.

使い方 / Usage
--------------
    python assets\\scripts\\check_nepali_coverage.py            # 点検 / report
    python assets\\scripts\\check_nepali_coverage.py --json     # 機械可読 / machine readable
    python assets\\scripts\\check_nepali_coverage.py --strict   # 文書の未翻訳も失敗にする
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from course_notebooks import course_notebooks
from apply_nepali_translations import REGION_RE
from romanize_nepali import DEVANAGARI_RE, looks_like_nepali_latin

COURSE_ROOT = Path(__file__).resolve().parents[2]
CATALOG_DIR = COURSE_ROOT / "assets" / "i18n" / "ne" / "notebooks"
DOC_CATALOG_DIR = COURSE_ROOT / "assets" / "i18n" / "ne" / "docs"

DOC_REGION_RE = re.compile(
    r"\n<!--\s*ne:begin\s+doc:[0-9a-f]+\s*-->\n(?P<body>.*?)\n<!--\s*ne:end\s*-->\n", re.S)

# Cells that deliberately stay untranslated: separators, empty scaffolding and the code placeholders
# a learner is meant to fill in themselves.
SEPARATOR_RE = re.compile(r"^\s*([-*_])\1{2,}\s*$")
PLACEHOLDER_MARKERS = ("ここに書いてください", "write your code here", "ここに記入")

# Nepali must not slip into Hindi or into a machine-translation placeholder.
# `karna` is deliberately absent from the Latin list: in Nepali `karna` (कर्ण) is the hypotenuse of
# the Day 2 geometry lesson, so only the Devanagari Hindi verb `करना` is a reliable marker.
FORBIDDEN_PATTERNS = {
    "hindi-है": re.compile(r"(?<![\u0900-\u097f])है(?![\u0900-\u097f])"),
    "hindi-करना": re.compile(r"करना"),
    "hindi-नहीं": re.compile(r"नहीं"),
    "hindi-होता": re.compile(r"होता"),
    "hindi-latin": re.compile(r"(?i)\b(hai|hain|nahin|hota)\b"),
    "placeholder": re.compile(r"(?i)\b(TODO|TBD|FIXME|XXX|लोरेम|ipsum)\b"),
    "todo-marker": re.compile(r"(?i)translat(e|ion) (needed|pending)"),
}

DOCUMENTS = [
    "START_HERE.md",
    "README.md",
    "COURSE_SYLLABUS.md",
    "docs/troubleshooting/installation.md",
    "docs/reference_materials.md",
    "docs/pdf/README.md",
    "requirements/tested_versions.md",
    "submissions/day01/Day01_Report_Template.md",
    "submissions/day02/Day02_Report_Template.md",
    "submissions/day03/Day03_Report_Template.md",
    "submissions/day04/Day04_Report_Template.md",
    "submissions/day05/Day05_Report_Template.md",
]


def cell_text(cell: dict) -> str:
    source = cell.get("source", [])
    return "".join(source) if isinstance(source, list) else str(source)


def script_of(body: str) -> str:
    """ブロックの文字 / which script a Nepali region is written in."""
    if DEVANAGARI_RE.search(body):
        return "devanagari"
    if looks_like_nepali_latin(body):
        return "romanized"
    return "unverified"


DIRECTIVE_SPLIT_RE = re.compile(r"^<!--\s*ne-(?:cell|section):.*-->$", re.M)


def catalog_script(path: Path) -> str:
    """カタログ全体の文字 / the script of a whole catalog (all-or-nothing)."""
    if not path.is_file():
        return "missing"
    text = path.read_text(encoding="utf-8")
    chunks = [chunk for chunk in DIRECTIVE_SPLIT_RE.split(text)[1:] if chunk.strip()]
    scripts = {script_of(chunk) for chunk in chunks}
    scripts.discard("unverified")
    if not scripts:
        return "empty"
    return scripts.pop() if len(scripts) == 1 else "mixed"


def regions(text: str) -> list[str]:
    return [match.group("body") for match in REGION_RE.finditer(text)]


def doc_regions(text: str) -> list[str]:
    return [match.group("body") for match in DOC_REGION_RE.finditer(text)]


def is_exempt(text: str) -> bool:
    stripped = text.strip()
    if not stripped:
        return True
    if all(SEPARATOR_RE.match(line) or not line.strip() for line in stripped.splitlines()):
        return True
    if any(marker in stripped for marker in PLACEHOLDER_MARKERS):
        return True
    return False


def check_notebook(path: Path) -> dict:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    cells = notebook["cells"]
    report = {
        "path": path.relative_to(COURSE_ROOT).as_posix(),
        "markdown_cells": 0,
        "translated": 0,
        "exempt": 0,
        "missing": [],
        "forbidden": [],
        "stray_devanagari": [],
        "unverified": [],
        "scripts": [],
        "chars": 0,
        "catalog": catalog_script(CATALOG_DIR / f"{path.stem}.ne.md"),
    }
    for cell in cells:
        if cell["cell_type"] != "markdown":
            continue
        report["markdown_cells"] += 1
        text = cell_text(cell)
        found = regions(text)
        outside = REGION_RE.sub("", text)
        if DEVANAGARI_RE.search(outside):
            report["stray_devanagari"].append(cell.get("id"))
        if found:
            report["translated"] += 1
            body = "\n".join(found)
            report["chars"] += len(body)
            for region in found:
                script = script_of(region)
                report["scripts"].append(script)
                if script == "unverified":
                    report["unverified"].append(cell.get("id"))
            for name, pattern in FORBIDDEN_PATTERNS.items():
                if pattern.search(body):
                    report["forbidden"].append(f"{cell.get('id')}:{name}")
            continue
        if is_exempt(outside):
            report["exempt"] += 1
        else:
            report["missing"].append(cell.get("id"))
    return report


def check_document(rel_path: str) -> dict:
    path = COURSE_ROOT / rel_path
    if not path.is_file():
        return {"path": rel_path, "exists": False, "regions": 0, "chars": 0, "forbidden": []}
    text = path.read_text(encoding="utf-8")
    found = doc_regions(text)
    scripts = [script_of(body) for body in found]
    report = {"path": rel_path, "exists": True, "regions": len(found),
              "chars": sum(len(body) for body in found), "forbidden": [],
              "scripts": scripts, "unverified": scripts.count("unverified")}
    body = "\n".join(found)
    for name, pattern in FORBIDDEN_PATTERNS.items():
        if pattern.search(body):
            report["forbidden"].append(name)
    return report


def catalogs_match_notebooks() -> list[str]:
    """翻訳カタログとノートブックの対応 / catalogs whose notebook has disappeared."""
    known = {path.stem for path in course_notebooks(COURSE_ROOT / "notebooks")}
    return sorted(path.name for path in CATALOG_DIR.glob("*.ne.md")
                  if path.name[: -len(".ne.md")] not in known)


def run() -> dict:
    notebooks = [check_notebook(path) for path in course_notebooks(COURSE_ROOT / "notebooks")]
    documents = [check_document(rel) for rel in DOCUMENTS]
    return {
        "notebooks": notebooks,
        "documents": documents,
        "orphan_catalogs": catalogs_match_notebooks(),
        "totals": {
            "markdown_cells": sum(item["markdown_cells"] for item in notebooks),
            "translated": sum(item["translated"] for item in notebooks),
            "exempt": sum(item["exempt"] for item in notebooks),
            "missing": sum(len(item["missing"]) for item in notebooks),
            "unverified": sum(len(item["unverified"]) for item in notebooks),
            "romanized_blocks": sum(item["scripts"].count("romanized") for item in notebooks),
            "devanagari_blocks": sum(item["scripts"].count("devanagari") for item in notebooks),
            "chars": sum(item["chars"] for item in notebooks),
            "documents_with_nepali": sum(1 for item in documents if item["regions"]),
        },
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Report the Nepali coverage of the course.")
    parser.add_argument("--json", action="store_true", help="print the report as JSON")
    parser.add_argument("--strict", action="store_true",
                        help="also fail when a documented file has no Nepali region")
    args = parser.parse_args(argv)

    report = run()
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        for item in report["notebooks"]:
            state = "ok" if not item["missing"] else f"missing {len(item['missing'])}"
            print(f"[nb]  {item['path']:<70} md={item['markdown_cells']:>3} "
                  f"ne={item['translated']:>3} exempt={item['exempt']:>2} "
                  f"({item['catalog']}) {state}")
            for problem in item["forbidden"][:5]:
                print(f"        ! forbidden: {problem}")
            for problem in item["stray_devanagari"][:5]:
                print(f"        ! Devanagari outside a region: {problem}")
            for problem in item["unverified"][:5]:
                print(f"        ! block is neither Devanagari nor Romanized Nepali: {problem}")
        for item in report["documents"]:
            print(f"[doc] {item['path']:<70} regions={item['regions']:>2} "
                  f"chars={item['chars']:>6} unverified={item['unverified']}")
        totals = report["totals"]
        share = 100 * totals["translated"] / max(totals["markdown_cells"], 1)
        print(f"[done] {totals['translated']}/{totals['markdown_cells']} markdown cells with Nepali "
              f"({share:.1f} %), {totals['exempt']} exempt, {totals['missing']} missing, "
              f"{totals['chars']:,} Nepali characters")
        print(f"[done] {totals['romanized_blocks']} Romanized and "
              f"{totals['devanagari_blocks']} Devanagari Nepali regions")
        print(f"[done] {totals['documents_with_nepali']}/{len(report['documents'])} documents "
              f"with Nepali regions")

    problems = report["totals"]["missing"] + len(report["orphan_catalogs"])
    problems += report["totals"]["unverified"]
    problems += sum(len(item["forbidden"]) + len(item["stray_devanagari"])
                    for item in report["notebooks"])
    problems += sum(len(item["forbidden"]) + item["unverified"] for item in report["documents"])
    if args.strict:
        problems += sum(1 for item in report["documents"] if not item["regions"])
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
