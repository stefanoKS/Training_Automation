"""Tests for the revised Day 7-9 curriculum.

The tests verify the actual curriculum, not merely that files exist: source-PDF
preservation, nine offline notebooks, independent calculations, sensor and PLC
compatibility, restart prevention, interlocks, camera optics and timing,
diagrams, the simulator, PDF structure and page budget, the timetable, the
support documents and the protected Days 1-6 baseline.

Run from the repository root or AI_Vision_Training:
    python -m pytest AI_Vision_Training/day07_09_support/tests -q
"""

from __future__ import annotations

import csv
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
    "day07": ("Day07_Automation_Concept_Mechanics", 14),
    "day08": ("Day08_Electrical_PLC", 14),
    "day09": ("Day09_AI_Camera_Imaging", 11),
}
LESSONS = (
    "Day07_01_Capacity_And_Effect",
    "Day07_02_Power_And_Actuators",
    "Day07_03_Selection_Specifications",
    "Day08_01_Electrical_Fundamentals",
    "Day08_02_Sensors_and_IO",
    "Day08_03_Ladder_Sequence",
    "Day09_01_Camera_Fundamentals",
    "Day09_02_Lighting_and_Imaging_Environment",
    "Day09_03_AI_Camera_System",
)
BILINGUAL_TOKENS = (
    "学習目標", "Learning objectives", "前提", "Prerequisites",
    "まとめ", "Summary", "完了チェックリスト", "Completion checklist",
    "よくある間違い", "Troubleshooting",
)


def manuscript(name: str) -> Path:
    for folder, _ in FOLDERS.values():
        path = NOTEBOOKS / folder / f"{name}.md"
        if path.is_file():
            return path
    raise FileNotFoundError(name)


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
    for obsolete in ("Day09_Communication_Commissioning", "Day07_Machine_Fundamentals",
                     "Day08_PLC_Control", "Day09_System_Integration"):
        assert not (NOTEBOOKS / obsolete).exists(), obsolete
    for obsolete in ("Day07_01_Requirements", "Day09_01_Industrial_Networking",
                     "Day09_02_Commissioning", "Day09_03_Automation_Proposal"):
        assert not list(NOTEBOOKS.glob(f"*/{obsolete}.ipynb")), obsolete
    assert not (ROOT / "week2").exists()


def test_manifest_and_fingerprints():
    manifest = builder.load_manifest()
    specs = builder.lesson_specs(manifest)
    assert [spec.name for spec in specs] == list(LESSONS)
    assert {spec.duration_min for spec in specs} == {80, 85, 135}
    assert [day["folder"] for day in manifest["days"]] == [folder for folder, _ in FOLDERS.values()]
    assert builder.stale_notebooks() == []


@pytest.mark.parametrize("name", LESSONS)
def test_notebook_structure_and_bilingual_content(name):
    parent = next(p for p in NOTEBOOKS.iterdir() if (p / f"{name}.ipynb").is_file())
    notebook = nbformat.read(parent / f"{name}.ipynb", as_version=4)
    nbformat.validate(notebook)
    codes = [cell for cell in notebook.cells if cell.cell_type == "code"]
    markdown = "\n".join("".join(cell.source) for cell in notebook.cells if cell.cell_type == "markdown")
    assert notebook.metadata["day07_09_source"] == f"{name}.md"
    assert notebook.metadata["day07_09_dependencies"]
    for token in BILINGUAL_TOKENS:
        assert token in markdown, (name, token)
    assert re.search(r"[\u3040-\u30ff\u4e00-\u9fff]", markdown)
    assert re.search(r"\b(?:the|and|with|for|is|are)\b", markdown, re.I)
    for link in re.findall(r"!\[[^\]]*\]\(([^)]+)\)", markdown):
        assert (parent / link).is_file(), (name, link)
    assert "安全" in markdown and re.search(r"safety", markdown, re.I)
    if name.startswith("Day07"):
        assert codes == [], "Day 7 notebooks must not contain executable cells"
        assert notebook.metadata["day07_09_executable_cells"] == 0
        assert "実行するプログラムはありません" in markdown or "実行するセルはありません" in markdown
    else:
        assert len(codes) >= 1


def test_every_notebook_executes_offline():
    result = subprocess.run(
        [sys.executable, str(SCRIPTS / "run_notebook_cells.py")],
        cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=300,
    )
    assert result.returncode == 0, result.stdout[-4000:] + result.stderr[-2000:]
    assert result.stdout.count("OK   ") == 9, result.stdout


# --------------------------------------------------------------------------- #
# Day 7: capacity, mechanics, economics
# --------------------------------------------------------------------------- #
def test_capacity_numbers():
    assert am.takt_time_s(420, 600) == pytest.approx(42.0)
    assert am.capacity_per_h(15) == pytest.approx(240.0)
    assert am.capacity_per_h(15, 2) == pytest.approx(480.0)
    assert am.required_rate_per_h(600, 420) == pytest.approx(85.714285, abs=1e-5)
    report = am.capacity_report()
    assert report["takt_s"] == pytest.approx(42.0)
    assert report["theoretical_per_h"] == pytest.approx(240.0)
    assert report["cycle_meets_takt"] is True
    assert am.capacity_table([10, 20])[1]["theoretical_per_h"] == pytest.approx(180.0)
    for bad in ((0, 600), (420, 0), (-1, 10)):
        with pytest.raises(ValueError):
            am.takt_time_s(*bad)
    with pytest.raises(ValueError):
        am.capacity_per_h(0)
    with pytest.raises(ValueError):
        am.capacity_per_h(15, 0)


def test_no_availability_or_oee_model_remains():
    for removed in ("effective_capacity_per_h", "describe_subnet",
                    "commissioning_matrix", "prefix_from_mask"):
        assert not hasattr(am, removed), removed
    text = "\n".join(manuscript(name).read_text(encoding="utf-8") for name in LESSONS[:3])
    assert "実力能力" not in text
    assert "×稼働率" not in text and "× 稼働率" not in text
    assert "稼働率" in text  # only as an explicit exclusion note


def test_mechanical_numbers():
    assert am.friction_force_n(8, 0.25) == pytest.approx(19.62)
    assert am.design_force_n(19.62, 2) == pytest.approx(39.24)
    assert am.theoretical_bore_mm(39.24, 0.4) == pytest.approx(11.1761, abs=1e-3)
    push = am.cylinder_force_n(20, 0.5)
    pull = am.cylinder_force_n(20, 0.5, 8)
    assert push == pytest.approx(157.08, abs=0.01)
    assert pull == pytest.approx(131.95, abs=0.01)
    assert push > pull
    with pytest.raises(ValueError):
        am.friction_force_n(-1, 0.25)
    with pytest.raises(ValueError):
        am.design_force_n(10, 0.5)
    with pytest.raises(ValueError):
        am.cylinder_force_n(16, 0.4, 16)
    with pytest.raises(ValueError):
        am.theoretical_bore_mm(10, 0)


def test_motor_numbers():
    torque = am.motor_torque_nm(60, 1200)
    assert torque == pytest.approx(0.4775, abs=1e-4)
    assert am.angular_speed_rad_s(1200) == pytest.approx(125.66, abs=0.01)
    assert am.reducer_output_speed_rpm(1200, 20) == pytest.approx(60)
    assert am.reducer_output_torque_nm(torque, 20, 1.0) == pytest.approx(9.5493, abs=1e-4)
    assert am.reducer_output_torque_nm(torque, 20, 0.90) == pytest.approx(8.5944, abs=1e-4)
    with pytest.raises(ValueError):
        am.motor_torque_nm(60, 0)
    with pytest.raises(ValueError):
        am.reducer_output_torque_nm(torque, 20, 0)
    with pytest.raises(ValueError):
        am.reducer_output_torque_nm(torque, 20, 1.2)


def test_payback_numbers():
    report = am.payback_report()
    assert report["minutes_per_day"] == pytest.approx(36.0)
    assert report["hours_per_year"] == pytest.approx(132.0)
    assert report["annual_value_jpy"] == pytest.approx(316_800)
    assert report["payback_years"] == pytest.approx(1.42045, abs=1e-4)
    with_cost = am.payback_report(annual_operating_cost_jpy=50_000)
    assert with_cost["annual_net_benefit_jpy"] == pytest.approx(266_800)
    assert with_cost["payback_years"] == pytest.approx(1.68666, abs=1e-4)
    with pytest.raises(ValueError):
        am.payback_years(0, 100)
    assert am.payback_years(450_000, 0) == math.inf
    assert am.payback_years(450_000, -1) == math.inf


# --------------------------------------------------------------------------- #
# Day 8: electrical, sensors, PLC
# --------------------------------------------------------------------------- #
def test_electrical_load_numbers():
    loads = am.training_power_budget()
    assert am.total_load_current_a(loads) == pytest.approx(0.80)
    report = am.load_report(loads, 0.25)
    assert report["total_power_w"] == pytest.approx(19.2)
    assert report["planning_current_a"] == pytest.approx(1.00)
    assert report["is_sizing_approval"] is False
    assert am.dc_power_w(24, 0.15) == pytest.approx(3.6)
    assert am.energy_kwh(100, 8) == pytest.approx(0.8)
    assert am.energy_cost_jpy(0.8, 30) == pytest.approx(24.0)
    with pytest.raises(ValueError):
        am.Load("bad", 1, 24, current_a=0.1, power_w=3).unit_current_a()
    with pytest.raises(ValueError):
        am.total_load_current_a([am.Load("x", -1, 24, current_a=0.1)])
    with pytest.raises(ValueError):
        am.dc_power_w(0, 1)


def test_npn_pnp_compatibility():
    pnp = am.plc_input_compatibility("PNP", "0V")
    assert pnp["compatible"] is True
    assert pnp["current_path"].startswith("+24V")
    assert pnp["is_detection_principle"] is False
    assert am.plc_input_compatibility("PNP", "+24V")["compatible"] is False
    assert am.plc_input_compatibility("NPN", "+24V")["compatible"] is True
    assert am.plc_input_compatibility("NPN", "0V")["compatible"] is False
    with pytest.raises(ValueError):
        am.plc_input_compatibility("XYZ", "0V")
    with pytest.raises(ValueError):
        am.plc_input_compatibility("PNP", "12V")


def test_sensor_no_nc_is_separate_from_npn_pnp():
    assert am.sensor_output_state(False, True) is True
    assert am.sensor_output_state(True, True) is False
    assert am.sensor_output_state(True, False) is True
    with pytest.raises(ValueError):
        am.sensor_output_state(1, True)  # type: ignore[arg-type]


def test_canonical_io_is_unambiguous():
    rows = list(am.CANONICAL_IO)
    assert am.validate_io(rows) == []
    by_address = {row["address"]: row for row in rows}
    assert by_address["X1"]["normal"].startswith("ON")
    assert "solenoid" in by_address["Y2"]["device"]
    assert "M1" in by_address
    broken = [dict(row) for row in rows]
    for row in broken:
        if row["address"] == "Y0":
            row["device"] = "solenoid valve"
        if row["address"] == "X1":
            row["normal"] = "OFF normally"
    problems = am.validate_io(broken)
    assert any("solenoid" in problem for problem in problems)
    assert any("X1" in problem for problem in problems)


def test_basic_seal_in_and_extended_gate():
    basic = am.BasicSealIn()
    assert basic.step(start=True, stop_ok=True) is True
    assert basic.step(start=False, stop_ok=True) is True
    assert basic.step(start=True, stop_ok=False) is False
    assert basic.step(start=True, stop_ok=True) is True  # the flaw the extended logic removes

    gate = am.StartGate()
    gate.power_on()
    assert gate.step(start=True)["run"] is False       # held START at power-up
    assert gate.step(start=False)["armed"] is True      # released and at position
    started = gate.step(start=True)
    assert started["run"] is True and started["start_edge"] is True
    assert gate.step(start=True, stop_ok=False)["run"] is False
    assert gate.step(start=True, stop_ok=True)["run"] is False  # restored while START held
    gate.step(start=False)
    assert gate.step(start=True)["run"] is True         # a new edge starts again


def test_start_gate_reset_is_not_a_start():
    gate = am.StartGate()
    gate.power_on()
    gate.fault = True
    result = gate.step(start=False, reset=True)
    assert result["fault"] is False and result["run"] is False
    gate.fault = True
    refused = gate.step(start=True, reset=True)
    assert refused["fault"] is True and refused["run"] is False


def test_pusher_sequence_stop_priority_and_restart():
    plc = am.PusherSequence()
    inputs = am.PlcInputs()
    plc.step(inputs, 100)
    inputs.start = True
    snap = plc.step(inputs, 100)
    assert snap.state == "READY" and snap.run
    inputs.start = False
    plc.step(inputs, 100)
    inputs.stop_ok = False
    snap = plc.step(inputs, 100)
    assert snap.state == "IDLE" and not snap.run and not snap.y2_extend_solenoid
    inputs.stop_ok = True
    assert plc.step(inputs, 100).run is False  # permission restored, START not pressed


def test_pusher_sequence_power_up_with_held_start():
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


def test_normal_cycle_and_invalid_transition():
    result = am.normal_cycle()
    final = result["final"]
    assert final.state == "COMPLETE" and final.cycle_count == 1
    for expected in ("READY", "EXTEND", "WAIT_EXTENDED", "RETRACT", "WAIT_RETRACTED", "COMPLETE"):
        assert expected in result["visited"]
    with pytest.raises(ValueError):
        am.PusherSequence().transition_to("COMPLETE")
    with pytest.raises(ValueError):
        am.PusherSequence().step(am.PlcInputs(), 0)
    with pytest.raises(ValueError):
        am.PusherSequence().step("not inputs", 100)  # type: ignore[arg-type]


def test_motion_timeout_and_sensor_conflict():
    plc = am.PusherSequence()
    plc.step(am.PlcInputs(retracted=True, extended=True), 100)
    assert plc.state == "FAULT" and plc.fault_code == "F002"
    plc = am.PusherSequence()
    released = am.PlcInputs()
    plc.step(released, 100)
    pressed = am.PlcInputs(start=True)
    plc.step(pressed, 100)
    pressed.start = False
    plc.step(pressed, 100)
    for _ in range(40):
        snap = plc.step(pressed, 100)
    assert snap.state == "FAULT" and snap.fault_code == "F001"


def test_fault_reset_never_starts_motion():
    plc = am.PusherSequence()
    plc.step(am.PlcInputs(retracted=True, extended=True), 100)
    assert plc.state == "FAULT"
    held = am.PlcInputs(start=True, retracted=False, extended=False)
    plc.step(held, 100, reset=False)
    assert plc.step(held, 100, reset=True).state == "FAULT"
    released = am.PlcInputs(start=False, retracted=True, extended=False)
    plc.step(released, 100, reset=False)
    snap = plc.step(released, 100, reset=True)
    assert snap.state == "IDLE" and snap.fault_code is None and not snap.run


def test_interlocks():
    drive = am.MotorInterlock()
    assert drive.step(True, False) == {"forward": True, "reverse": False, "conflict": False}
    assert drive.step(False, True) == {"forward": False, "reverse": True, "conflict": False}
    both = drive.step(True, True)
    assert both["forward"] is False and both["reverse"] is False and both["conflict"] is True
    stopped = drive.step(True, False, stop_ok=False)
    assert stopped["forward"] is False and stopped["reverse"] is False
    assert am.interlock_allows({"product": True, "retracted": True}, True) is True
    assert am.interlock_allows({"product": False, "retracted": True}, True) is False
    assert am.interlock_allows({"product": True}, False) is False
    with pytest.raises(ValueError):
        am.interlock_allows({}, True)


# --------------------------------------------------------------------------- #
# Day 9: camera optics and inspection timing
# --------------------------------------------------------------------------- #
def test_camera_optics_numbers():
    sampling = am.object_space_sampling_mm_per_px(240, 1920)
    assert sampling == pytest.approx(0.125)
    assert am.defect_size_px(0.5, sampling) == pytest.approx(4.0)
    assert am.defect_size_px(1.0, sampling) == pytest.approx(8.0)
    assert am.motion_blur_mm(1000, 0.001) == pytest.approx(1.0)
    assert am.motion_blur_px(1000, 0.001, sampling) == pytest.approx(8.0)
    assert am.exposure_time_s(1, 1000, sampling) == pytest.approx(0.000125)
    assert am.line_rate_lps(1000, 0.125) == pytest.approx(8000.0)
    assert am.frame_interval_move_mm(1000, 30) == pytest.approx(33.3333, abs=1e-3)
    for call in (
        lambda: am.object_space_sampling_mm_per_px(0, 1920),
        lambda: am.defect_size_px(0.5, 0),
        lambda: am.motion_blur_mm(-1, 0.001),
        lambda: am.exposure_time_s(1, 0, 0.125),
        lambda: am.line_rate_lps(1000, 0),
        lambda: am.frame_interval_move_mm(1000, 0),
    ):
        with pytest.raises(ValueError):
            call()


def test_inspection_decision_never_turns_invalid_into_ok():
    assert am.inspection_decision("OK") == "OK"
    assert am.inspection_decision("NG") == "NG"
    assert am.inspection_decision(None) == "INVALID"
    assert am.inspection_decision("maybe") == "INVALID"
    assert am.inspection_decision("OK", image_available=False) == "INVALID"
    assert am.inspection_decision("OK", inference_ok=False) == "INVALID"
    assert am.inspection_decision("OK", communication_ok=False) == "INVALID"
    assert set(am.INSPECTION_RESULTS) == {"OK", "NG", "INVALID"}


def test_imaging_checklist_is_bilingual():
    items = am.imaging_checklist()
    assert len(items) >= 12
    for item in items:
        assert item["item_ja"] and item["item_en"]
        assert re.search(r"[\u3040-\u30ff\u4e00-\u9fff]", item["item_ja"])
        assert re.search(r"[a-z]{3}", item["item_en"])


# --------------------------------------------------------------------------- #
# diagrams, simulator
# --------------------------------------------------------------------------- #
def test_diagrams_are_bilingual_and_referenced():
    lesson_text = "\n".join(manuscript(name).read_text(encoding="utf-8") for name in LESSONS)
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
    assert total == 39
    assert len(list(DIAGRAMS.glob("day07/*.svg"))) == 14
    assert len(list(DIAGRAMS.glob("day08/*.svg"))) == 14
    assert len(list(DIAGRAMS.glob("day09/*.svg"))) == 11
    for stale in ("D07-15", "D08-15", "D09-12"):
        assert not list(DIAGRAMS.glob(f"day0*/{stale}.svg")), stale


def test_offline_html_simulator():
    html = (SUPPORT / "simulations" / "sim_plc_sequence.html").read_text(encoding="utf-8")
    for banned in ("fetch(", "XMLHttpRequest", "WebSocket", "http://", "https://", "<script src"):
        assert banned not in html, banned
    assert "<noscript>" in html
    assert "LOGIC-START" in html and "LOGIC-END" in html
    assert (SUPPORT / "simulations" / "fallback" / "sim_plc_sequence.png").stat().st_size > 20_000
    assert not (SUPPORT / "simulations" / "fallback" / "sim_commissioning.png").exists()
    if shutil.which("node"):
        result = subprocess.run(["node", str(SUPPORT / "tests" / "run_simulation_logic_tests.js")],
                                cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
        assert result.returncode == 0, result.stderr
        assert "SIMULATION LOGIC TESTS PASSED" in result.stdout


# --------------------------------------------------------------------------- #
# PDFs
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("day", ("Day07", "Day08", "Day09"))
def test_pdf_contains_searchable_bilingual_content(day):
    path = PDF_DIR / f"{day}_explanation_ja_en.pdf"
    assert path.is_file() and path.stat().st_size > 400_000
    reader = PdfReader(str(path))
    assert len(reader.pages) >= 12
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


def test_day09_pdf_within_page_limit():
    reader = PdfReader(str(PDF_DIR / "Day09_explanation_ja_en.pdf"))
    assert len(reader.pages) <= 19
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    for removed in ("サブネット", "試運転ゲート", "自動化提案", "Modbus"):
        assert removed not in text, removed


def test_day07_and_day08_pdfs_are_shorter_than_before():
    day07 = len(PdfReader(str(PDF_DIR / "Day07_explanation_ja_en.pdf")).pages)
    day08 = len(PdfReader(str(PDF_DIR / "Day08_explanation_ja_en.pdf")).pages)
    assert day07 < 58, day07
    assert day08 < 60, day08


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
# timetable and support documents
# --------------------------------------------------------------------------- #
def test_syllabus_rows_and_totals():
    text = (ROOT / "COURSE_SYLLABUS_DAY07_09.md").read_text(encoding="utf-8")
    assert "530分" in text
    assert "08:00–16:50" in text
    for slot in ("08:00–09:00", "09:00–10:20", "10:35–12:00", "12:50–13:50",
                 "13:50–15:10", "15:25–16:20", "16:20–16:50"):
        assert slot in text, slot
    for name in ("07-01", "07-02", "07-03", "08-01", "08-02", "08-03", "09-01", "09-02", "09-03"):
        assert name in text, name
    assert "120分" in text and "300分" in text and "30分" in text and "50分" in text


@pytest.mark.parametrize("day", ("Day07", "Day08", "Day09"))
def test_worksheets_and_answer_keys_are_short_and_consistent(day):
    sheet = (SUPPORT / "worksheets" / f"{day}_Student_Worksheet_ja_en.md").read_text(encoding="utf-8")
    key = (SUPPORT / "worksheets" / f"{day}_Answer_Key_ja_en.md").read_text(encoding="utf-8")
    tasks = re.findall(r"^## (T\d+)", sheet, re.M)
    assert tasks, day
    assert len(tasks) <= 3, (day, tasks)
    assert "安全境界" in sheet and "Safety boundary" in sheet
    assert "答え / Answer" in key or "答え / answer" in key
    for task in tasks:
        assert task in key, (day, task)


def test_answer_key_numbers_are_reproducible():
    day07 = (SUPPORT / "worksheets" / "Day07_Answer_Key_ja_en.md").read_text(encoding="utf-8")
    assert "42 秒/個" in day07 and "240 個/時" in day07
    assert "316,800" in day07 and "266,800" in day07 and "1.69" in day07
    assert "9.81 N" in day07 and "19.62 N" in day07 and "7.07 mm" in day07
    day08 = (SUPPORT / "worksheets" / "Day08_Answer_Key_ja_en.md").read_text(encoding="utf-8")
    assert "0.60 A" in day08 and "14.4 W" in day08 and "0.72 A" in day08
    day09 = (SUPPORT / "worksheets" / "Day09_Answer_Key_ja_en.md").read_text(encoding="utf-8")
    assert "0.125 mm/px" in day09 and "4 px" in day09 and "8 px" in day09
    assert am.payback_report(annual_operating_cost_jpy=50_000)["payback_years"] == pytest.approx(1.68666, abs=1e-4)


@pytest.mark.parametrize("day", ("day07", "day08", "day09"))
def test_instructor_guides_match_the_curriculum(day):
    guide = (ROOT / "docs" / "instructor" / f"{day}_instructor_guide.md").read_text(encoding="utf-8")
    for heading in ("学習目標 / learning objectives", "必要な教材 / required materials",
                    "午前の説明", "午後のフォロー", "よくある誤解", "理解確認の質問",
                    "ワークシートとの対応", "安全上の制約", "時間配分"):
        assert heading in guide, (day, heading)
    number = day[3:]
    assert f"Day{number}_" in guide or f"{number}-01" in guide


def test_curriculum_source_map_covers_every_page():
    rows = list(csv.DictReader((SUPPORT / "curriculum_source_map.csv").open(encoding="utf-8")))
    assert len(rows) == 51
    assert sorted(int(row["pdf_page"]) for row in rows) == list(range(1, 52))
    allowed = {"REQUIRED", "SUPPLEMENTARY", "INCORPORATED_ELSEWHERE",
               "REPLACED_WITH_CORRECTED_CONTENT", "REFERENCE_ONLY",
               "CORRECTED_AND_INCORPORATED", "REMOVED_FROM_ACTIVE",
               "SUPERSEDED_BY_NEW_AI_CAMERA"}
    assert {row["coverage_status"] for row in rows} <= allowed
    assert all(row["target_day"] and row["target_notebook"] for row in rows)
    active = [row for row in rows if row["coverage_status"] in
              ("REQUIRED", "CORRECTED_AND_INCORPORATED", "REPLACED_WITH_CORRECTED_CONTENT")]
    assert active, "some source material must remain required"
    for row in rows:
        if row["coverage_status"] == "SUPERSEDED_BY_NEW_AI_CAMERA":
            assert row["target_notebook"].startswith("Day09_")


def test_glossary_and_quick_references():
    glossary = (SUPPORT / "worksheets" / "Glossary_ja_en.md").read_text(encoding="utf-8")
    compact = (SUPPORT / "worksheets" / "Glossary_day09_ja_en.md").read_text(encoding="utf-8")
    assert glossary.count("|") > 100 and "タクトタイム" in glossary and "視野" in glossary
    assert len(compact) < len(glossary) / 3
    for word in ("サブネット", "試運転"):
        assert word not in glossary, word
    for day in ("day07", "day08", "day09"):
        text = (SUPPORT / "reference_data" / f"quick_reference_{day}.md").read_text(encoding="utf-8")
        assert "学習用" in text
        assert text.count("|") > 20


def test_obsolete_lessons_are_not_referenced_in_navigation():
    for path in (ROOT / "README.md", ROOT / "START_HERE.md",
                 SUPPORT / "README_ja_en.md", ROOT / "COURSE_SYLLABUS_DAY07_09.md"):
        text = path.read_text(encoding="utf-8")
        assert "Day09_Communication_Commissioning" not in text, path
        assert "Day07_01_Requirements" not in text, path
    assert "Day09_AI_Camera_Imaging" in (ROOT / "README.md").read_text(encoding="utf-8")


def test_protected_days_1_to_6_baseline():
    manifest = (SUPPORT / "reference_data" / "protected_baseline_hashes.txt").read_text(encoding="utf-8-sig")
    entries = [line.split("  ", 1) for line in manifest.splitlines() if line.strip()]
    assert len(entries) > 300
    for digest, relative in entries:
        path = REPO / relative
        assert path.is_file(), relative
        current = subprocess.check_output(["git", "hash-object", str(path)], cwd=REPO, text=True).strip()
        assert current == digest, f"protected file changed: {relative}"
