"""Focused Day 6 isolation, teaching-content and export contracts."""

import hashlib
import json
import re
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
LESSONS = (
    "Day06_01_LLM_Agent_Harness",
    "Day06_02_Ideas_and_Requirements",
    "Day06_03_Prompting_and_Agents",
    "Day06_04_Testing_and_Handover",
)


@pytest.mark.parametrize("name", LESSONS)
def test_notebook_is_current_read_only_bilingual_and_offline(name):
    source = ROOT / "lessons" / f"{name}.md"
    notebook = json.loads((ROOT / "lessons" / f"{name}.ipynb").read_text(encoding="utf-8"))
    assert notebook["nbformat"] == 4
    assert notebook["metadata"]["day06_source_sha256"] == hashlib.sha256(source.read_bytes()).hexdigest()
    assert len(notebook["cells"]) >= 5
    assert all(cell["cell_type"] == "markdown" for cell in notebook["cells"])
    text = "\n".join("".join(cell["source"]) for cell in notebook["cells"])
    assert re.search(r"[\u3040-\u30ff\u4e00-\u9fff]", text)
    assert re.search(r"\b(?:the|and|with|for)\b", text, re.I)
    assert "Nepali" not in text and "Tamang" not in text
    assert "../DAY06_SYLLABUS_ja_en.md" in text
    for image in re.findall(r"!\[[^\]]+\]\(([^)]+)\)", text):
        assert not image.startswith(("http:", "https:"))
        assert (source.parent / image).is_file()


def test_figures_exist_and_have_accessible_titles():
    figures = ROOT / "assets" / "diagrams"
    for index in range(1, 15):
        path = figures / f"D06-{index:02}.svg"
        root = ET.parse(path).getroot()
        assert root.tag.endswith("svg")
        assert root.find("{http://www.w3.org/2000/svg}title") is not None
        assert root.find("{http://www.w3.org/2000/svg}desc") is not None


def test_case_study_mockup_matches_approved_scope():
    root = ET.parse(ROOT / "assets" / "diagrams" / "D06-08.svg").getroot()
    labels = " ".join(element.text or "" for element in root.iter() if element.tag.endswith("text"))
    for required in ("塩ビシート不良記録アプリ", "PVC-EX-001", "PVC-EX-002",
                     "CSV", "ロット", "検査日時", "黒点", "傷", "すじ", "Validation"):
        assert required in labels
    assert "Photo" not in labels and "SAMPLE-PVC" not in labels


def test_case_study_and_syllabus_agree():
    lesson = (ROOT / "lessons" / f"{LESSONS[1]}.md").read_text(encoding="utf-8")
    spec = (ROOT / "examples" / "inspection_app_spec_ja_en.md").read_text(encoding="utf-8")
    tests = (ROOT / "examples" / "example_test_cases_ja_en.md").read_text(encoding="utf-8")
    for content in (lesson, spec, tests):
        assert "PVC-EX-001" in content and "PVC-EX-002" in content
        assert "lot_id,inspected_at,defect_type,description,remarks" in content
    syllabus = (ROOT / "DAY06_SYLLABUS_ja_en.md").read_text(encoding="utf-8")
    rows = re.findall(r"^\| \d\d:\d\d–\d\d:\d\d \| (\d+) \| .* \| (.*?) \|$", syllabus, re.M)
    assert len(rows) == 14
    totals = {}
    for duration, category in rows:
        key = category.split(" / ")[0]
        totals[key] = totals.get(key, 0) + int(duration)
    assert totals == {"講師": 120, "必須": 300, "休憩": 30, "昼食": 50, "提出": 30}


def test_supporting_materials_and_prompts():
    prompts = (ROOT / "examples" / "example_agent_prompts_ja_en.md").read_text(encoding="utf-8")
    for letter in "ABCDEF":
        assert re.search(rf"^## {letter}\.", prompts, re.M)
    assert prompts.count("**いつ / When:**") == 6
    assert prompts.count("**変える所 / Customize:**") == 6
    for relative in (
        "instructor/day06_instructor_guide_ja_en.md",
        "worksheets/Day06_Student_Worksheet_ja_en.md",
        "worksheets/Day06_Assessment_Rubric_ja_en.md",
        "examples/example_agent_conversation_ja_en.md",
        "examples/example_handover_ja_en.md",
    ):
        assert (ROOT / relative).is_file()


def test_pdf_contains_all_lessons_and_figure_images():
    pdf = ROOT / "pdf" / "Day06_explanation_ja_en.pdf"
    reader = PdfReader(str(pdf))
    assert len(reader.pages) >= 8
    text = "\n".join(page.extract_text() for page in reader.pages)
    titles = ["LLMs, agents and harnesses", "Ideas and requirements",
              "Communicating with coding agents", "Verification, safety and handover"]
    normalized = re.sub(r"\s+", " ", text)
    offsets = [normalized.index(title) for title in titles]
    assert offsets == sorted(offsets)
    assert "塩ビシート" in text and "PVC-EX-001" in text
    assert sum(len(page.images) for page in reader.pages) >= 14


def test_exporter_is_isolated_and_protected_tracked_files_are_unchanged():
    exporter = (ROOT / "scripts" / "export_day06_pdf.py").read_text(encoding="utf-8")
    assert 'OUTPUT = ROOT / "pdf" / "Day06_explanation_ja_en.pdf"' in exporter
    changed = subprocess.check_output(
        ["git", "diff", "--name-only", "HEAD", "--", "AI_Vision_Training"],
        cwd=REPO, text=True,
    ).splitlines()
    assert not changed, f"Protected tracked Week 1 file changed: {changed}"
