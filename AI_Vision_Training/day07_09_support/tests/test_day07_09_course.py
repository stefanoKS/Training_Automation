"""Tests for the Day 7-9 replacement curriculum.

The tests verify the actual curriculum, not merely that files exist:
source PDF preservation, nine offline notebooks, independent calculations,
PLC/sequence behaviour, commissioning statuses, diagrams, simulations, PDFs,
timetable arithmetic and the protected Days 1-6 baseline.

Run from the repository root or AI_Vision_Training:
    python -m pytest AI_Vision_Training/day07_09_support/tests -q
"""

from __future__ import annotations

import json
import math
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
PDF_DIR = ROOT / "docs" / "pdf"
PDF = ROOT / "docs" / "reference" / "自動化設備製作研修_5日間_詳細版_受講者用.pdf"
SOURCE_SHA256 = "3380c2b67e148cd9a71b0f9071963744f3b0acba7491b309708b0f31183707ae"

sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(SUPPORT / "examples"))
import automation_models as am  # noqa: E402
import build_day07_09_notebooks as builder  # noqa: E402

FOLDERS = {
    "day07": ("Day07_Automation_Concept_Mechanics", 9),
    "day08": ("Day08_Electrical_PLC", 11),
    "day09": ("Day09_Communication_Commissioning", 9),
}
LESSONS = (
    "Day07_01_Requirements",
    "Day07_02_Mechanical_Architecture",
    "Day07_03_Equipment_Selection",
    "Day08_01_Electrical_Fundamentals",
    "Day08_02_Sensors_and_IO",
    "Day08_03_Ladder_Sequence",
    "Day09_01_Industrial_Networking",
    "Day09_02_Commissioning",
    "Day09_03_Automation_Proposal",
)


# --------------------------------------------------------------------------- #
# source and repository structure
# --------------------------------------------------------------------------- #
def test_source_pdf_is_preserved():
    assert PDF.is_file()
    assert builder.sha256_file(PDF) == SOURCE_SHA256
    assert len(PdfReader(str(PDF)).pages) == 51


def test_nine_notebooks_and_no_duplicate_active_course():
    assert len(LESSONS) == 9
    for name in LESSONS:
        matches = list(NOTEBOOKS.glob(f"*/{name}.ipynb"))
        assert len(matches) == 1, (name, matches)
        assert matches[0].with_suffix(".md").is_file()
    for old in ("Day07_Machine_Fundamentals", "Day08_PLC_Control", "Day09_System_Integration"):
        assert not (NOTEBOOKS / old).exists(), old
    assert not (ROOT / "week2").exists()
    assert not (NOTEBOOKS / "Day07_Machine_Fundamentals").exists()


def test_manifest_and_fingerprints():
    manifest = builder.load_manifest()
    specs = builder.lesson_specs(manifest)
    assert [spec.name for spec in specs] == list(LESSONS)
    assert {spec.duration_min for spec in specs} == {80, 85, 135}
    assert builder.stale_notebooks() == []


@pytest.mark.parametrize("name", LESSONS)
def test_notebook_structure_and_bilingual_content(name):
    parent = next(p for p in NOTEBOOKS.iterdir() if (p / f"{name}.ipynb").is_file())
    notebook = nbformat.read(parent / f"{name}.ipynb", as_version=4)
    nbformat.validate(notebook)
    codes = [cell for cell in notebook.cells if cell.cell_type == "code"]
    markdown = "\n".join("".join(cell.source) for cell in notebook.cells if cell.cell_type == "markdown")
    assert len(codes) >= 3
    assert notebook.metadata["day07_09_source"] == f"{name}.md"
    assert notebook.metadata["day07_09_dependencies"]
    for token in ("学習目標", "Learning objectives", "前提", "Prerequisites", "まとめ", "Summary",
                  "完了チェックリスト", "Completion checklist", "トラブル", "Troubleshooting"):
        assert token in markdown, (name, token)
    assert re.search(r"[\u3040-\u30ff\u4e00-\u9fff]", markdown)
    assert re.search(r"\b(?:the|and|with|for|is|are)\b", markdown, re.I)
    for link in re.findall(r"!\[[^\]]*\]\(([^)]+)\)", markdown):
        assert (parent / link).is_file(), (name, link)
    assert "安全" in markdown and re.search(r"safety", markdown, re.I)


def test_every_notebook_executes_offline():
    result = subprocess.run(
        [sys.executable, str(SCRIPTS / "run_notebook_cells.py")],
        cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=300,
    )
    assert result.returncode == 0, result.stdout[-4000:] + result.stderr[-2000:]
    assert result.stdout.count("OK   ") == 9, result.stdout


# --------------------------------------------------------------------------- #
# independent numerical checks
# --------------------------------------------------------------------------- #
def test_capacity_numbers():
    assert am.takt_time_s(420, 600) == pytest.approx(42.0)
    assert am.theoretical_capacity_per_h(15) == pytest.approx(240.0)
    assert am.effective_capacity_per_h(15, 0.85, 0.98) == pytest.approx(199.92)
    assert am.takt_time_s(450, 900) == pytest.approx(30.0)
    assert am.effective_capacity_per_h(20, 0.80, 0.97) == pytest.approx(139.68)
    with pytest.raises(ValueError):
        am.takt_time_s(0, 600)
    with pytest.raises(ValueError):
        am.effective_capacity_per_h(15, 85, 0.98)


def test_mechanical_numbers():
    assert am.friction_force_n(8, 0.25) == pytest.approx(19.62)
    assert am.design_force_n(19.62, 2) == pytest.approx(39.24)
    assert am.theoretical_bore_mm(39.24, 0.4) == pytest.approx(11.1761, abs=1e-3)
    push = am.cylinder_force_n(20, 0.4)
    pull = am.cylinder_force_n(20, 0.4, 8)
    assert push == pytest.approx(125.66, abs=0.02)
    assert pull == pytest.approx(105.56, abs=0.02)
    assert push > pull
    with pytest.raises(ValueError):
        am.friction_force_n(-1, 0.25)
    with pytest.raises(ValueError):
        am.design_force_n(10, 0.5)
    with pytest.raises(ValueError):
        am.cylinder_force_n(16, 0.4, 16)


def test_motor_numbers():
    torque = am.motor_torque_nm(60, 1200)
    assert torque == pytest.approx(0.4775, abs=1e-4)
    assert am.reducer_output_speed_rpm(1200, 20) == pytest.approx(60)
    assert am.reducer_output_torque_nm(torque, 20, 1.0) == pytest.approx(9.5493, abs=1e-4)
    assert am.reducer_output_torque_nm(torque, 20, 0.90) == pytest.approx(8.5944, abs=1e-4)
    with pytest.raises(ValueError):
        am.motor_torque_nm(60, 0)
    with pytest.raises(ValueError):
        am.reducer_output_torque_nm(torque, 20, 0)
    with pytest.raises(ValueError):
        am.reducer_output_torque_nm(torque, 20, 1.2)


def test_electrical_load_numbers():
    loads = am.pdf_electrical_example()
    assert loads[0].unit_current_a() == pytest.approx(0.125)
    assert am.total_load_current_a(loads) == pytest.approx(0.73)
    report = am.load_report(loads, 0.25)
    assert report["planning_current_a"] == pytest.approx(0.9125)
    assert report["is_sizing_approval"] is False
    with pytest.raises(ValueError):
        am.Load("bad", 1, 24, current_a=0.1, power_w=3).unit_current_a()
    with pytest.raises(ValueError):
        am.total_load_current_a([am.Load("x", -1, 24, current_a=0.1)])


def test_payback_numbers():
    report = am.payback_report()
    assert report["minutes_per_day"] == pytest.approx(36.0)
    assert report["annual_value_jpy"] == pytest.approx(316_800)
    assert report["payback_years"] == pytest.approx(1.42045, abs=1e-4)
    with pytest.raises(ValueError):
        am.payback_years(0, 100)
    assert am.payback_report(annual_operating_cost_jpy=400_000)["payback_years"] == math.inf


def test_canonical_io_is_unambiguous():
    rows = list(am.CANONICAL_IO)
    assert am.validate_io(rows) == []
    by_address = {row["address"]: row for row in rows}
    assert by_address["Y1"]["device"].startswith("delayed")
    assert "solenoid" in by_address["Y2"]["device"]
    assert by_address["X1"]["normal"].startswith("ON")


# --------------------------------------------------------------------------- #
# PLC and sequence behaviour
# --------------------------------------------------------------------------- #
def _fresh():
    plc = am.PusherSequence()
    plc.step(am.PlcInputs(), 100)
    return plc


def test_start_release_self_holding_and_stop():
    plc = _fresh()
    inputs = am.PlcInputs()
    inputs.start = True
    snap = plc.step(inputs, 100)
    assert snap.state == "READY" and snap.run and snap.y0_run_lamp
    inputs.start = False
    snap = plc.step(inputs, 100)
    assert snap.run and snap.state == "EXTEND"
    snap = plc.step(inputs, 100)
    assert snap.state == "WAIT_EXTENDED"
    inputs.stop_ok = False
    snap = plc.step(inputs, 100)
    assert snap.state == "IDLE" and not snap.run and snap.t0_ms == 0 and not snap.y2_extend_solenoid


def test_stop_during_extension_and_timer():
    plc = _fresh()
    inputs = am.PlcInputs()
    inputs.start = True
    plc.step(inputs, 100)
    inputs.start = False
    plc.step(inputs, 100)
    inputs.stop_ok = False
    snap = plc.step(inputs, 100)
    assert snap.state == "IDLE" and not snap.y2_extend_solenoid
    # timer path
    plc = _fresh()
    inputs = am.PlcInputs()
    inputs.start = True
    plc.step(inputs, 100)
    inputs.start = False
    for _ in range(10):
        plc.step(inputs, 100)
    inputs.stop_ok = False
    snap = plc.step(inputs, 100)
    assert snap.t0_ms == 0 and not snap.y1_delayed_lamp


def test_timer_threshold_and_reset():
    plc = am.PusherSequence()
    am.normal_cycle(plc)
    inputs = am.PlcInputs()
    while plc.t0_ms < 2999:
        plc.step(inputs, 1)
    snap = plc.snapshot()
    assert snap.t0_ms == 2999 and not snap.y1_delayed_lamp
    snap = plc.step(inputs, 1)
    assert snap.t0_ms == 3000 and snap.y1_delayed_lamp
    inputs.stop_ok = False
    snap = plc.step(inputs, 1)
    assert snap.t0_ms == 0 and not snap.y1_delayed_lamp


def test_normal_cycle_and_position_confirmation():
    result = am.normal_cycle()
    final = result["final"]
    assert final.state == "COMPLETE" and final.cycle_count == 1
    states = result["visited"]
    for expected in ("READY", "EXTEND", "WAIT_EXTENDED", "RETRACT", "WAIT_RETRACTED", "COMPLETE"):
        assert expected in states


def test_motion_timeout_and_sensor_conflict():
    assert am.run_scenario("sensor_stuck_off")["final"].fault_code == "F001"
    assert am.run_scenario("retract_stuck")["final"].fault_code == "F003"
    assert am.run_scenario("motion_slow")["final"].fault_code == "F001"
    assert am.run_scenario("sensor_conflict")["final"].fault_code == "F002"
    assert am.run_scenario("sensor_stuck_off")["final"].state == "FAULT"


def test_fault_reset_never_starts_motion():
    plc = am.PusherSequence()
    plc.step(am.PlcInputs(retracted=True, extended=True), 100)
    assert plc.state == "FAULT"
    held = am.PlcInputs(start=True, retracted=False, extended=False)
    plc.step(held, 100, reset=False)
    assert plc.step(held, 100, reset=True).state == "FAULT"
    released = am.PlcInputs(start=False, retracted=True, extended=False)
    plc.step(released, 100, reset=False)
    plc.step(released, 100, reset=False)
    snap = plc.step(released, 100, reset=True)
    assert snap.state == "IDLE" and snap.fault_code is None and not snap.run and not snap.y2_extend_solenoid


def test_power_restore_with_held_start_and_new_start():
    plc = am.PusherSequence()
    plc.power_on()
    held = am.PlcInputs(start=True)
    for _ in range(20):
        snap = plc.step(held, 100)
    assert snap.state == "IDLE" and not snap.run
    held.start = False
    plc.step(held, 100)
    held.start = True
    assert plc.step(held, 100).state == "READY"


def test_repeat_cycle_and_invalid_transition():
    plc = am.PusherSequence()
    am.normal_cycle(plc)
    released = am.PlcInputs()
    plc.step(released, 100)
    released.start = True
    snap = plc.step(released, 100)
    assert snap.state == "READY" and snap.cycle_count == 2
    with pytest.raises(ValueError):
        am.PusherSequence().transition_to("COMPLETE")
    with pytest.raises(ValueError):
        am.PusherSequence().step(am.PlcInputs(), 0)


def test_commissioning_matrix_statuses_and_fields():
    records = am.commissioning_matrix()
    statuses = {record.test_id: record.status for record in records}
    assert sum(status == "PASS" for status in statuses.values()) == 10
    assert statuses["T11"] == "BLOCKED" and statuses["T12"] == "BLOCKED"
    for record in records:
        for field in ("test_id", "requirement_id", "preconditions", "procedure", "expected",
                      "actual", "status", "evidence", "operator", "date", "corrective_action"):
            assert getattr(record, field) is not None
        if record.status != "PASS":
            assert record.status in ("FAIL", "NOT TESTED", "BLOCKED")
    with pytest.raises(ValueError):
        am.TestRecord("X", "R", "", "", "", "", "OK", "", "", "")


# --------------------------------------------------------------------------- #
# networking
# --------------------------------------------------------------------------- #
def test_subnet_slash24_and_slash25():
    assert am.describe_subnet("192.168.10.10", 24)["network"] == "192.168.10.0"
    assert am.describe_subnet("192.168.10.10", 24)["broadcast"] == "192.168.10.255"
    assert am.describe_subnet("192.168.10.10", 24)["usable_hosts"] == 254
    assert am.describe_subnet("192.168.10.130", 25)["network"] == "192.168.10.128"
    assert am.describe_subnet("192.168.10.130", 25)["first_host"] == "192.168.10.129"
    assert am.describe_subnet("192.168.10.130", 25)["last_host"] == "192.168.10.254"
    assert am.same_subnet("192.168.10.130", "192.168.10.200", 25) is True
    assert am.same_subnet("192.168.10.130", "192.168.10.20", 25) is False
    assert am.prefix_from_mask("255.255.255.128") == 25
    with pytest.raises(ValueError):
        am.prefix_from_mask("255.255.0.255")
    with pytest.raises(ValueError):
        am.parse_ipv4("192.168.10.256")
    with pytest.raises(ValueError):
        am.parse_ipv4("192.168.010.1")


def test_subnet_edge_cases():
    assert am.describe_subnet("10.0.0.0", 31)["usable_hosts"] == 2
    assert am.describe_subnet("10.0.0.1", 31)["exclusion_rule"].startswith("/31")
    assert am.describe_subnet("10.0.0.1", 32)["usable_hosts"] == 1
    assert am.mask_from_prefix(0) == "0.0.0.0"


# --------------------------------------------------------------------------- #
# diagrams, simulations and PDFs
# --------------------------------------------------------------------------- #
def test_diagrams_are_bilingual_and_referenced():
    lesson_text = "\n".join(
        (NOTEBOOKS / folder / f"{name}.md").read_text(encoding="utf-8")
        for folder, _ in FOLDERS.values() for name in LESSONS if (NOTEBOOKS / folder / f"{name}.md").is_file()
    )
    total = 0
    for day_key, (folder, count) in FOLDERS.items():
        for index in range(1, count + 1):
            path = DIAGRAMS / day_key / f"D{day_key[3:]}-{index:02d}.svg"
            assert path.is_file(), path
            root = ET.parse(path).getroot()
            assert root.tag.endswith("svg")
            assert root.find("{http://www.w3.org/2000/svg}title") is not None
            assert root.find("{http://www.w3.org/2000/svg}desc") is not None
            labels = [element.text or "" for element in root.iter() if element.tag.endswith("text")]
            assert len(labels) >= 10, path
            assert sum(bool(re.search(r"[\u3040-\u30ff\u4e00-\u9fff]", label)) for label in labels) >= 4, path
            assert sum(bool(re.search(r"[A-Za-z]{3}", label)) for label in labels) >= 4, path
            assert all("\ufffd" not in label and "??" not in label for label in labels), path
            assert path.name in lesson_text, path
            png = SUPPORT / "reference_data" / "diagram_png" / day_key / f"{path.stem}.png"
            assert png.is_file() and png.stat().st_size > 20_000, png
            total += 1
    assert total == 29
    for old in ("D07-10.svg", "D08-12.svg", "D09-10.svg"):
        assert not any(DIAGRAMS.glob(f"day0*/{old}")), old


def test_offline_html_simulator():
    html = (SUPPORT / "simulations" / "sim_plc_sequence.html").read_text(encoding="utf-8")
    for banned in ("fetch(", "XMLHttpRequest", "WebSocket", "http://", "https://", "<script src"):
        assert banned not in html, banned
    assert "<noscript>" in html
    assert "LOGIC-START" in html and "LOGIC-END" in html
    assert (SUPPORT / "simulations" / "fallback" / "sim_plc_sequence.png").stat().st_size > 20_000
    if shutil.which("node"):
        result = subprocess.run(["node", str(SUPPORT / "tests" / "run_simulation_logic_tests.js")],
                                cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
        assert result.returncode == 0, result.stderr
        assert "SIMULATION LOGIC TESTS PASSED" in result.stdout


@pytest.mark.parametrize("day", ("Day07", "Day08", "Day09"))
def test_pdf_contains_searchable_bilingual_content(day):
    path = PDF_DIR / f"{day}_explanation_ja_en.pdf"
    assert path.is_file() and path.stat().st_size > 500_000
    reader = PdfReader(str(path))
    assert len(reader.pages) >= 20
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    assert "目次 / Contents" in text
    assert "付録A 公式・確認カード" in text
    assert "付録B 技術用語集" in text
    assert "付録C 参考資料" in text
    assert re.search(r"[\u3040-\u30ff\u4e00-\u9fff]", text)
    assert re.search(r"\b(?:the|and|of)\b", text, re.I)
    assert "\ufffd" not in text
    assert "](" not in text
    assert not re.search(r"</?(?:div|span|br|b|i|font)\b", text, re.I)
    assert sum(len(page.images) for page in reader.pages) >= 4
    assert not re.search(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\s*\n\s*\d{1,3}\b", text)


def test_pdf_pages_render_non_blank():
    pdfium = pytest.importorskip("pypdfium2")
    for day in ("Day07", "Day08", "Day09"):
        document = pdfium.PdfDocument(str(PDF_DIR / f"{day}_explanation_ja_en.pdf"))
        for index in range(len(document)):
            image = document[index].render(scale=0.25).to_pil().convert("L")
            pixels = list(image.getdata())
            mean = sum(pixels) / len(pixels)
            spread = (sum((pixel - mean) ** 2 for pixel in pixels) / len(pixels)) ** 0.5
            assert spread > 4, f"{day} page {index + 1} looks blank"


# --------------------------------------------------------------------------- #
# timetable, support documents and protected baseline
# --------------------------------------------------------------------------- #
def test_syllabus_rows_and_totals():
    syllabus = (ROOT / "COURSE_SYLLABUS_DAY07_09.md").read_text(encoding="utf-8")
    rows = re.findall(r"^\| (\d\d:\d\d)–(\d\d:\d\d) \| (\d+) \| .* \| (.*?) \|$", syllabus, re.M)
    assert len(rows) == 40, len(rows)
    for block in (rows[i:i + 10] for i in range(0, 40, 10)):
        totals: dict[str, int] = {}
        for start, end, duration, kind in block:
            minutes = (int(end[:2]) * 60 + int(end[3:])) - (int(start[:2]) * 60 + int(start[3:]))
            assert minutes == int(duration)
            totals[kind.split(" / ")[0]] = totals.get(kind.split(" / ")[0], 0) + int(duration)
        assert totals == {"講師": 120, "必須": 300, "休憩": 30, "昼食": 50, "提出": 30}
        assert sum(totals.values()) == 530
    assert "08:00–16:50" in syllabus


def test_support_documents_exist():
    for path in (
        SUPPORT / "README_ja_en.md",
        SUPPORT / "SOURCES_AND_LICENSES.md",
        SUPPORT / "curriculum_source_map.csv",
        SUPPORT / "worksheets" / "Day07_Student_Worksheet_ja_en.md",
        SUPPORT / "worksheets" / "Day08_Student_Worksheet_ja_en.md",
        SUPPORT / "worksheets" / "Day09_Student_Worksheet_ja_en.md",
        SUPPORT / "worksheets" / "Day07_Answer_Key_ja_en.md",
        SUPPORT / "worksheets" / "Day08_Answer_Key_ja_en.md",
        SUPPORT / "worksheets" / "Day09_Answer_Key_ja_en.md",
        SUPPORT / "worksheets" / "Day07_09_Assessment_Rubric_ja_en.md",
        SUPPORT / "worksheets" / "Glossary_ja_en.md",
        ROOT / "docs" / "instructor" / "day07_instructor_guide.md",
        ROOT / "docs" / "instructor" / "day08_instructor_guide.md",
        ROOT / "docs" / "instructor" / "day09_instructor_guide.md",
        ROOT / "docs" / "reference" / "Automation_Equipment_PDF_Errata_ja_en.md",
        ROOT / "docs" / "reviews" / "Day07_09_PDF_Migration_Audit.md",
        ROOT / "docs" / "reviews" / "Day07_09_Release_Review.md",
    ):
        assert path.is_file(), path
        assert path.stat().st_size > 1200, path


def test_curriculum_source_map_covers_every_page():
    import csv
    rows = list(csv.DictReader((SUPPORT / "curriculum_source_map.csv").open(encoding="utf-8")))
    assert len(rows) == 51
    assert sorted(int(row["pdf_page"]) for row in rows) == list(range(1, 52))
    allowed = {"REQUIRED", "SUPPLEMENTARY", "INCORPORATED_ELSEWHERE",
               "REPLACED_WITH_CORRECTED_CONTENT", "REFERENCE_ONLY"}
    assert {row["coverage_status"] for row in rows} <= allowed
    assert all(row["target_day"] and row["target_notebook"] for row in rows)


def test_protected_days_1_to_6_baseline():
    manifest = (SUPPORT / "reference_data" / "protected_baseline_hashes.txt").read_text(encoding="utf-8-sig")
    entries = [line.split("  ", 1) for line in manifest.splitlines() if line.strip()]
    assert len(entries) > 300
    for digest, relative in entries:
        path = REPO / relative
        assert path.is_file(), relative
        current = subprocess.check_output(["git", "hash-object", str(path)], cwd=REPO, text=True).strip()
        assert current == digest, f"protected file changed: {relative}"
