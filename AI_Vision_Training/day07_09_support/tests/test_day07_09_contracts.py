"""Contract tests for the Day 7-9 course, diagrams, simulations, PDFs and timetable."""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import nbformat
import pytest
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
REPO = ROOT.parent
SUPPORT = ROOT / "day07_09_support"
SCRIPTS = SUPPORT / "scripts"
NOTEBOOKS = ROOT / "notebooks"
DIAGRAMS = ROOT / "assets" / "diagrams"

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
DAY_FOLDERS = {"day07": "Day07_Machine_Fundamentals",
               "day08": "Day08_PLC_Control",
               "day09": "Day09_System_Integration"}
LESSONS = tuple(name for names in DAYS.values() for name in names)

sys.path.insert(0, str(SCRIPTS))
import engineering_examples as calc  # noqa: E402


def all_lesson_text() -> str:
    return "\n".join((NOTEBOOKS / folder / f"{name}.md").read_text(encoding="utf-8")
                     for folder, names in DAYS.items() for name in names)


# ----------------------------------------------------------------- repository
def test_protected_files_match_baseline():
    manifest = (SUPPORT / "reference_data" / "protected_baseline_hashes.txt").read_text(encoding="utf-8-sig")
    entries = [line.split("  ", 1) for line in manifest.splitlines() if line.strip()]
    assert len(entries) > 300
    for digest, path in entries:
        current = subprocess.check_output(["git", "hash-object", path], cwd=REPO, text=True).strip()
        assert current == digest, f"protected file changed: {path}"


def test_only_authorised_paths_changed():
    status = subprocess.check_output(
        ["git", "status", "--porcelain", "--untracked-files=all"], cwd=REPO, text=True
    ).splitlines()
    allowed = (
        "AI_Vision_Training/COURSE_SYLLABUS_DAY07_09.md",
        "AI_Vision_Training/notebooks/Day07_",
        "AI_Vision_Training/notebooks/Day08_",
        "AI_Vision_Training/notebooks/Day09_",
        "AI_Vision_Training/assets/diagrams/day07/",
        "AI_Vision_Training/assets/diagrams/day08/",
        "AI_Vision_Training/assets/diagrams/day09/",
        "AI_Vision_Training/day07_09_support/",
        "AI_Vision_Training/docs/instructor/day07_",
        "AI_Vision_Training/docs/instructor/day08_",
        "AI_Vision_Training/docs/instructor/day09_",
        "AI_Vision_Training/docs/pdf/Day07_",
        "AI_Vision_Training/docs/pdf/Day08_",
        "AI_Vision_Training/docs/pdf/Day09_",
        "AI_Vision_Training/docs/reviews/Day07_09_",
        "AI_Vision_Training/day07_09_support/simulations/fallback/",
    )
    changed = [line[3:].strip().strip('"') for line in status]
    assert changed, "expected Day 7-9 additions"
    for path in changed:
        assert path.startswith(allowed), path


def test_no_week2_tree_and_no_duplicate_notebooks():
    assert not (ROOT / "week2").exists()
    for folder in DAYS:
        notebooks = sorted((NOTEBOOKS / folder).glob("*.ipynb"))
        assert len(notebooks) == 3, notebooks
    for name in LESSONS:
        assert len(list(NOTEBOOKS.glob(f"*/{name}.ipynb"))) == 1, name
        assert len(list(NOTEBOOKS.glob(f"*/{name}.md"))) == 1, name


# ----------------------------------------------------------------- notebooks
@pytest.mark.parametrize("name", LESSONS)
def test_notebook_matches_manuscript_and_is_read_only(name):
    folder = next(f for f, names in DAYS.items() if name in names)
    directory = NOTEBOOKS / folder
    source = directory / f"{name}.md"
    raw = (directory / f"{name}.ipynb").read_text(encoding="utf-8")
    notebook = nbformat.from_dict(json.loads(raw))
    nbformat.validate(notebook)
    assert notebook["metadata"]["day07_09_source"] == f"{name}.md"
    assert notebook["metadata"]["day07_09_source_sha256"] == hashlib.sha256(source.read_bytes()).hexdigest()
    assert len(notebook["cells"]) >= 8
    assert all(cell["cell_type"] == "markdown" for cell in notebook["cells"])
    ids = [cell["id"] for cell in notebook["cells"]]
    assert len(ids) == len(set(ids))
    text = "\n".join("".join(cell["source"]) for cell in notebook["cells"])
    assert re.search(r"[\u3040-\u30ff\u4e00-\u9fff]", text)
    assert re.search(r"\b(?:the|and|with|for)\b", text, re.I)
    assert "../../COURSE_SYLLABUS_DAY07_09.md" in text
    for image in re.findall(r"!\[[^\]]+\]\(([^)]+)\)", text):
        assert not image.startswith(("http:", "https:"))
        assert (directory / image).is_file(), image


def test_every_lesson_has_the_required_teaching_parts():
    assert len(LESSONS) == 9
    for folder, names in DAYS.items():
        for name in names:
            text = (NOTEBOOKS / folder / f"{name}.md").read_text(encoding="utf-8")
            for marker in ("到達目標", "Objectives", "演習", "Exercises", "まとめ", "Summary",
                           "完了条件", "Completion criteria", "安全"):
                assert marker in text, (name, marker)
            figures = re.findall(r"!\[[^\]]+\]\(([^)]+)\)", text)
            assert len(figures) >= 2, name
            assert "仮定" in text and "架空" in text, name


def test_case_study_and_safety_boundaries_are_consistent():
    text = all_lesson_text()
    assert text.count("連続塩ビシート検査機") >= 2
    for concept in ("有効なAI結果", "タイムアウト", "古い結果", "安全機能", "リスクアセスメント"):
        assert concept in text
    assert "無効な結果をOKにしない" in text or "有効なAI結果がないまま" in text
    assert "通常のラダー" in text


# ----------------------------------------------------------------- diagrams
def test_thirty_six_bilingual_diagrams():
    total = 0
    for day, prefix in (("day07", "D07"), ("day08", "D08"), ("day09", "D09")):
        folder = DIAGRAMS / day
        lesson_text = "\n".join(
            (NOTEBOOKS / DAY_FOLDERS[day] / f"{name}.md").read_text(encoding="utf-8")
            for name in DAYS[DAY_FOLDERS[day]]
        )
        for index in range(1, 13):
            path = folder / f"{prefix}-{index:02}.svg"
            assert path.is_file(), path
            root = ET.parse(path).getroot()
            assert root.tag.endswith("svg")
            assert root.get("viewBox") == f"0 0 {root.get('width')} {root.get('height')}"
            assert root.find("{http://www.w3.org/2000/svg}title") is not None
            assert root.find("{http://www.w3.org/2000/svg}desc") is not None
            labels = [element.text or "" for element in root.iter() if element.tag.endswith("text")]
            assert len(labels) >= 6, path
            assert sum(bool(re.search(r"[\u3040-\u30ff\u4e00-\u9fff]", label)) for label in labels) >= 5, path
            assert sum(bool(re.search(r"[A-Za-z]{3}", label)) for label in labels) >= 5, path
            assert all("\ufffd" not in label and "??" not in label for label in labels), path
            assert path.name in lesson_text, path.name
            total += 1
    assert total == 36


# ----------------------------------------------------------------- numbers
def test_numeric_examples_meet_the_specification():
    assert calc.roller_circumference_mm(100) == pytest.approx(314.159265, abs=1e-3)
    assert calc.roller_surface_speed_m_per_min(100, 100) == pytest.approx(31.416, abs=1e-3)
    assert calc.roller_surface_speed_m_per_min(80, 200) == pytest.approx(50.265, abs=1e-3)
    assert calc.pixel_scale_mm_per_px(600, 4096) == pytest.approx(0.146484375, abs=1e-9)
    assert calc.pixel_scale_mm_per_px(400, 2048) == pytest.approx(0.1953125, abs=1e-9)
    assert calc.line_rate_lines_per_s(30, 0.2) == pytest.approx(2500)
    assert calc.line_rate_lines_per_s(60, 0.1) == pytest.approx(10000)
    assert calc.image_data_rate_bytes_s(4096, 2500) == 10_240_000
    assert calc.image_data_rate_bytes_s(2048, 5000) == 10_240_000
    assert calc.travel_mm(0.5, 0.12) == pytest.approx(60)
    assert calc.travel_mm(0.4, 0.15) == pytest.approx(60)
    assert calc.scale_linear(5, 0, 10, 0, 100) == pytest.approx(50)
    assert calc.scale_linear(7.5, 0, 10, 0, 200) == pytest.approx(150)
    assert calc.scale_linear(12, 4, 20, 0, 100) == pytest.approx(50)
    assert calc.encoder_counts_per_turn(1000, 4) == 4000
    assert calc.encoder_counts_per_turn(500, 2) == 1000
    assert calc.encoder_deg_per_count(1000, 4) == pytest.approx(0.09)
    assert calc.encoder_mm_per_count(100, 1000, 4) == pytest.approx(0.0785398, abs=1e-7)
    with pytest.raises(ValueError):
        calc.encoder_counts_per_turn(1000, 3)


def test_ladder_and_protocol_logic_reference_behaviour():
    assert calc.on_delay(True, 1999, 2000) == (False, 1999)
    assert calc.on_delay(True, 2000, 2000) == (True, 2000)
    assert calc.on_delay(False, 1500, 2000) == (False, 0.0)
    assert calc.counter_step(0, True, 3, False) == (1, False)
    assert calc.counter_step(2, True, 3, False) == (3, True)
    assert calc.counter_step(2, False, 3, False) == (2, False)
    assert calc.counter_step(2, False, 3, True) == (0, False)
    assert calc.decide_result("OK", 101) == "ACCEPT_OK"
    assert calc.decide_result("NG", 101) == "ACCEPT_NG"
    assert calc.decide_result("INVALID", 101) == "HOLD"
    assert calc.decide_result("TIMEOUT", 101) == "HOLD"
    assert calc.decide_result("OK", 101, valid=False) == "HOLD"
    assert calc.decide_result("OK", 100, last_accepted_id=101) == "REJECT_STALE"
    assert calc.decide_result("DUPLICATE", 101, last_accepted_id=101) == "REJECT_DUPLICATE"
    assert calc.decide_result("OK", 101, last_accepted_id=101) == "REJECT_DUPLICATE"


def test_manuscripts_quote_the_verified_numbers():
    day07 = (NOTEBOOKS / DAY_FOLDERS["day07"]).glob("*.md")
    day08 = (NOTEBOOKS / DAY_FOLDERS["day08"]).glob("*.md")
    day09 = (NOTEBOOKS / DAY_FOLDERS["day09"]).glob("*.md")
    text07 = "\n".join(p.read_text(encoding="utf-8") for p in day07)
    text08 = "\n".join(p.read_text(encoding="utf-8") for p in day08)
    text09 = "\n".join(p.read_text(encoding="utf-8") for p in day09)
    for token in ("31.416", "0.09°", "0.07854", "150 kPa", "50.27"):
        assert token in text07, token
    for token in ("2.0 s", "停止要求を優先", "立ち上がり", "100 ms"):
        assert token in text08, token
    for token in ("0.146484", "2,500 lines/s", "10.24 MB/s", "60 mm", "81.92 Mb/s"):
        assert token in text09, token


# ----------------------------------------------------------------- simulations
def test_simulations_are_offline_and_have_fallbacks():
    html_files = sorted((SUPPORT / "simulations").glob("sim_*.html"))
    assert len(html_files) == 6
    banned = ("fetch(", "XMLHttpRequest", "WebSocket", "http://", "https://", "<script src")
    for path in html_files:
        html = path.read_text(encoding="utf-8")
        for token in banned:
            assert token not in html, (path.name, token)
        assert "<noscript>" in html, path.name
        assert "LOGIC-START" in html and "LOGIC-END" in html
        assert (SUPPORT / "simulations" / "fallback" / f"{path.stem}.png").stat().st_size > 5000
    assert (SUPPORT / "simulations" / "fallback").glob("*.png")


@pytest.mark.skipif(shutil.which("node") is None, reason="node is unavailable")
def test_simulation_logic_suite_passes():
    result = subprocess.run(
        [shutil.which("node"), str(SUPPORT / "tests" / "run_simulation_logic_tests.js")],
        cwd=ROOT, capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stderr
    assert "SIMULATION LOGIC TESTS PASSED" in result.stdout


# ----------------------------------------------------------------- PDFs
@pytest.mark.parametrize("day", ("Day07", "Day08", "Day09"))
def test_pdf_contains_modules_figures_and_both_languages(day):
    path = ROOT / "docs" / "pdf" / f"{day}_explanation_ja_en.pdf"
    assert path.is_file() and path.stat().st_size > 200_000
    reader = PdfReader(str(path))
    assert len(reader.pages) >= 30
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    compact = re.sub(r"\s+", " ", text)
    assert not re.search(r"\?{2,}", text), "mangled text in PDF"
    assert re.search(r"[\u3040-\u30ff\u4e00-\u9fff]", text)
    assert re.search(r"\b(?:the|and|of)\b", text, re.I)
    assert "目次 / Contents" in compact
    assert "公式・確認カード" in compact
    assert "技術用語集" in compact
    assert "参考資料 / References" in compact
    assert "架空の学習用資料 / fictional training material" in compact
    assert sum(len(page.images) for page in reader.pages) >= 8
    figures = sum(len(page.images) for page in reader.pages)
    assert figures >= 10


def test_pdf_rendered_pages_are_not_blank():
    pdfium = pytest.importorskip("pypdfium2")
    for day in ("Day07", "Day08", "Day09"):
        document = pdfium.PdfDocument(str(ROOT / "docs" / "pdf" / f"{day}_explanation_ja_en.pdf"))
        for index in (0, len(document) // 2, len(document) - 1):
            image = document[index].render(scale=0.4).to_pil().convert("L")
            pixels = list(image.getdata())
            mean = sum(pixels) / len(pixels)
            spread = (sum((p - mean) ** 2 for p in pixels) / len(pixels)) ** 0.5
            assert spread > 8, f"{day} page {index + 1} looks blank"


# ----------------------------------------------------------------- timetable
def test_syllabus_totals_and_day_tables():
    syllabus = (ROOT / "COURSE_SYLLABUS_DAY07_09.md").read_text(encoding="utf-8")
    rows = re.findall(r"^\| (\d\d:\d\d)–(\d\d:\d\d) \| (\d+) \| .* \| (.*?) \|$", syllabus, re.M)
    assert len(rows) == 40, len(rows)
    blocks = [rows[index:index + 10] for index in range(0, 40, 10)]
    for block in blocks:
        totals: dict[str, int] = {}
        for start, end, duration, kind in block:
            totals[kind.split(" / ")[0]] = totals.get(kind.split(" / ")[0], 0) + int(duration)
            minutes = (int(end[:2]) * 60 + int(end[3:])) - (int(start[:2]) * 60 + int(start[3:]))
            assert minutes == int(duration), (start, end, duration)
        assert totals == {"講師": 120, "必須": 300, "休憩": 30, "昼食": 50, "提出": 30}, totals
        assert sum(totals.values()) == 530
    assert "08:00–16:50" in syllabus
    assert "12:00–12:50" in syllabus


# ----------------------------------------------------------------- support docs
def test_support_documents_exist():
    for path in (
        SUPPORT / "README_ja_en.md",
        SUPPORT / "SOURCES_AND_LICENSES.md",
        SUPPORT / "worksheets" / "Day07_Student_Worksheet_ja_en.md",
        SUPPORT / "worksheets" / "Day08_Student_Worksheet_ja_en.md",
        SUPPORT / "worksheets" / "Day09_Student_Worksheet_ja_en.md",
        SUPPORT / "worksheets" / "Day07_Answer_Key_ja_en.md",
        SUPPORT / "worksheets" / "Day08_Answer_Key_ja_en.md",
        SUPPORT / "worksheets" / "Day09_Answer_Key_ja_en.md",
        SUPPORT / "worksheets" / "Day07_09_Assessment_Rubric_ja_en.md",
        SUPPORT / "worksheets" / "Glossary_ja_en.md",
        SUPPORT / "examples" / "example_machine_component_map_ja_en.md",
        SUPPORT / "examples" / "example_plc_io_table_ja_en.md",
        SUPPORT / "examples" / "example_result_record_ja_en.md",
        ROOT / "docs" / "instructor" / "day07_instructor_guide.md",
        ROOT / "docs" / "instructor" / "day08_instructor_guide.md",
        ROOT / "docs" / "instructor" / "day09_instructor_guide.md",
        ROOT / "docs" / "reviews" / "Day07_09_PreImplementation_Audit.md",
    ):
        assert path.is_file(), path
        assert path.stat().st_size > 800, path


def test_instructor_guides_cover_the_fifteen_required_topics():
    topics = ("学習目標", "前提", "時間割", "午前", "午後", "図", "シミュレーション",
              "質問", "誤解", "正しい説明", "演習", "トラブル", "安全", "オフライン", "評価")
    for day in ("day07", "day08", "day09"):
        text = (ROOT / "docs" / "instructor" / f"{day}_instructor_guide.md").read_text(encoding="utf-8")
        for topic in topics:
            assert topic in text, (day, topic)
