"""Verify the independent Day 6 course, prices, figures, PDF and Week 1 isolation."""

import hashlib
import json
import re
import subprocess
import xml.etree.ElementTree as ET
from decimal import Decimal
from pathlib import Path

import nbformat
import pytest
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
REPO = ROOT.parent
LESSON_DIR = ROOT / "notebooks" / "Day06_LLM_Agents"
SUPPORT = ROOT / "day06_support"
LESSONS = (
    "Day06_01_LLM_Fundamentals",
    "Day06_02_Agents_and_Harness",
    "Day06_03_Idea_to_Specification",
    "Day06_04_Prompting_and_Execution",
    "Day06_05_Verification_and_Cost",
)


@pytest.mark.parametrize("name", LESSONS)
def test_notebook_is_valid_current_bilingual_and_read_only(name):
    source = LESSON_DIR / f"{name}.md"
    notebook = json.loads((LESSON_DIR / f"{name}.ipynb").read_text(encoding="utf-8"))
    nbformat.validate(nbformat.from_dict(notebook))
    assert notebook["metadata"]["day06_source_sha256"] == hashlib.sha256(source.read_bytes()).hexdigest()
    assert len(notebook["cells"]) >= 5
    assert all(cell["cell_type"] == "markdown" for cell in notebook["cells"])
    text = "\n".join("".join(cell["source"]) for cell in notebook["cells"])
    assert re.search(r"[\u3040-\u30ff\u4e00-\u9fff]", text)
    assert re.search(r"\b(?:the|and|with|for)\b", text, re.I)
    assert "Nepali" not in text and "Tamang" not in text
    assert "../../COURSE_SYLLABUS_DAY06.md" in text
    for image in re.findall(r"!\[[^\]]+\]\(([^)]+)\)", text):
        assert not image.startswith(("http:", "https:"))
        assert (source.parent / image).is_file()


def test_figures_are_bilingual_and_all_used():
    figures = ROOT / "assets" / "diagrams" / "day06"
    lesson_text = "\n".join(p.read_text(encoding="utf-8") for p in LESSON_DIR.glob("*.md"))
    paths = [figures / f"D06-{index:02}.svg" for index in range(1, 23)]
    paths += sorted(figures.glob("D06-M*.svg"))
    assert len(paths) == 25
    for path in paths:
        diagram = ET.parse(path).getroot()
        assert diagram.tag.endswith("svg")
        assert diagram.find("{http://www.w3.org/2000/svg}title") is not None
        assert diagram.find("{http://www.w3.org/2000/svg}desc") is not None
        labels = [element.text or "" for element in diagram.iter() if element.tag.endswith("text")]
        assert len(labels) >= 5
        assert sum(bool(re.search(r"[\u3040-\u9fff]", x)) for x in labels) >= 5, path
        assert sum(bool(re.search(r"[A-Za-z]{3}", x)) for x in labels) >= 5, path
        assert all("\ufffd" not in label and "??" not in label for label in labels), path
        assert any(re.search(r"[A-Za-z]{3}", x) for x in labels)
        assert path.name in lesson_text


def test_case_study_and_syllabus_agree():
    lesson = (LESSON_DIR / f"{LESSONS[2]}.md").read_text(encoding="utf-8")
    spec = (SUPPORT / "examples" / "inspection_app_spec_ja_en.md").read_text(encoding="utf-8")
    cases = (SUPPORT / "examples" / "example_test_cases_ja_en.md").read_text(encoding="utf-8")
    for content in (lesson, spec, cases):
        for field in ("PVC-EX-001", "PVC-EX-002",
                      "lot_id,inspected_at,defect_type,description,remarks"):
            assert field in content
    syllabus = (ROOT / "COURSE_SYLLABUS_DAY06.md").read_text(encoding="utf-8")
    rows = re.findall(r"^\| \d\d:\d\d–\d\d:\d\d \| (\d+) \| .* \| (.*?) \|$", syllabus, re.M)
    assert len(rows) == 13
    totals = {}
    for duration, category in rows:
        key = category.split(" / ")[0]
        totals[key] = totals.get(key, 0) + int(duration)
    assert totals == {"講師": 120, "必須": 300, "休憩": 30, "昼食": 50, "提出": 30}


def test_prompts_support_and_pricing_source_are_complete():
    prompts = (SUPPORT / "examples" / "example_agent_prompts_ja_en.md").read_text(encoding="utf-8")
    for letter in "ABCDEFGHI":
        assert re.search(rf"^## {letter}\.", prompts, re.M)
    assert prompts.count("**いつ / When:**") == 9
    for path in (
        ROOT / "docs" / "instructor" / "day06_instructor_guide.md",
        SUPPORT / "worksheets" / "Day06_Student_Worksheet_ja_en.md",
        SUPPORT / "worksheets" / "Day06_Assessment_Rubric_ja_en.md",
        ROOT / "docs" / "reviews" / "Day06_PreRevision_Audit.md",
        SUPPORT / "pricing" / "pricing_sources_2026-11-22.md",
    ):
        assert path.is_file()
    data = json.loads((SUPPORT / "pricing" / "pricing_snapshot_2026-11-22.json").read_text(encoding="utf-8"))
    sources = (SUPPORT / "pricing" / "pricing_sources_2026-11-22.md").read_text(encoding="utf-8")
    notebook = (LESSON_DIR / f"{LESSONS[4]}.ipynb").read_text(encoding="utf-8")
    assert data["verified_on"] == "2026-11-22" and data["unit"] == "per 1 million tokens"
    assert len(set(row["provider"] for row in data["entries"])) >= 8
    for row in data["entries"]:
        assert row["model_id"] and row["source"].startswith("https://")
        assert row["condition"] and row["caveat"]
        assert row["model_id"] in sources and row["model_id"] in notebook
        assert row["source"] in sources
        for key in ("input", "output"):
            assert isinstance(row[key], (float, int)) and row[key] >= 0
        assert row["cached_input"] is None or row["cached_input"] >= 0


def test_hypothetical_cost_examples():
    import sys

    sys.path.insert(0, str(SUPPORT / "scripts"))
    from render_pricing import token_cost

    assert token_cost(100000, 20000, "2", "10") == Decimal("0.4")
    steps = ((20000, 2000), (30000, 3000), (40000, 10000), (25000, 5000))
    assert sum(token_cost(i, o, "2", "10") for i, o in steps) == Decimal("0.43")
    with pytest.raises(ValueError):
        token_cost(-1, 100, "2", "10")


def test_pdf_contains_five_modules_and_local_figures():
    reader = PdfReader(str(ROOT / "docs" / "pdf" / "Day06_explanation_ja_en.pdf"))
    assert len(reader.pages) >= 40
    text = re.sub(r"\s+", " ", "\n".join(page.extract_text() for page in reader.pages))
    titles = ("LLM fundamentals", "Agents and harnesses", "From idea to specification",
              "Prompting and supervised execution", "Verification, costs, safety and handover")
    offsets = [text.lower().index(title.lower()) for title in titles]
    assert offsets == sorted(offsets)
    assert "塩ビシート" in text and "PVC-EX-001" in text
    assert "API価格の公式出典" in text and "2026-11-22" in text
    assert sum(len(page.images) for page in reader.pages) >= 25


def test_protected_files_and_no_duplicate_active_lessons():
    assert not (ROOT / "week2" / "day06" / "lessons").exists()
    changed = subprocess.check_output(
        ["git", "diff", "HEAD", "--name-only", "--", "AI_Vision_Training"], cwd=REPO, text=True,
    ).splitlines()
    allowed = (
        "AI_Vision_Training/week2/day06/",
        "AI_Vision_Training/notebooks/Day06_LLM_Agents/",
        "AI_Vision_Training/assets/diagrams/day06/",
        "AI_Vision_Training/day06_support/",
        "AI_Vision_Training/submissions/day06/",
        "AI_Vision_Training/COURSE_SYLLABUS_DAY06.md",
        "AI_Vision_Training/docs/reviews/Day06_",
        "AI_Vision_Training/docs/instructor/day06_instructor_guide.md",
        "AI_Vision_Training/docs/pdf/Day06_explanation_ja_en.pdf",
    )
    assert all(path.startswith(allowed) for path in changed), changed
