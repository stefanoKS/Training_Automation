"""解説 PDF のテスト / Explanation-PDF tests.

PDF が「読める資料」になっているかを、ファイルの存在だけでなく中身で確かめます。
These tests check the PDFs by content, not just by existence: page count, Japanese text that
survived the export, a table of contents, the sources page, and no empty pages.
"""

from __future__ import annotations

import re
import hashlib
from pathlib import Path

import pytest

COURSE_ROOT = Path(__file__).resolve().parents[2]
PDF_DIR = COURSE_ROOT / "docs" / "pdf"

DAY_PDFS = {
    "Day01": 40,
    "Day02": 40,
    "Day03": 30,
    "Day04": 30,
    "Day05": 30,
    "Week1": 150,
}

JP_RE = re.compile(r"[\u3040-\u30ff\u4e00-\u9fff]")


def _reader(name: str):
    pypdf = pytest.importorskip("pypdf", reason="PDF tooling is optional (requirements/pdf.txt)")
    path = PDF_DIR / f"{name}_explanation_ja_en.pdf"
    assert path.is_file(), f"missing {path.name}; run assets/scripts/export_explanations_pdf.py"
    return pypdf.PdfReader(str(path))


@pytest.mark.parametrize("name", sorted(DAY_PDFS))
def test_pdf_exists_with_enough_pages(name: str) -> None:
    reader = _reader(name)
    assert len(reader.pages) >= DAY_PDFS[name], (
        f"{name}: {len(reader.pages)} pages is suspiciously short")


@pytest.mark.parametrize("name", sorted(DAY_PDFS))
def test_pdf_contains_japanese_text(name: str) -> None:
    reader = _reader(name)
    text = "\n".join((page.extract_text() or "") for page in reader.pages)
    japanese = len(JP_RE.findall(text))
    assert japanese > 5000, f"{name}: only {japanese} Japanese characters survived the export"


@pytest.mark.parametrize("name", sorted(DAY_PDFS))
def test_pdf_has_a_table_of_contents_and_a_sources_page(name: str) -> None:
    reader = _reader(name)
    text = "\n".join((page.extract_text() or "") for page in reader.pages)
    assert "目次 / Table of contents" in text, f"{name}: no table of contents"
    assert "出典と参照 / Sources and references" in text, f"{name}: no sources page"
    assert "この資料について / About this companion" in text, f"{name}: no 'about' page"


@pytest.mark.parametrize("name", sorted(DAY_PDFS))
def test_pdf_has_no_blank_pages(name: str) -> None:
    reader = _reader(name)
    blank = [index + 1 for index, page in enumerate(reader.pages)
             if len((page.extract_text() or "").strip()) < 20]
    assert not blank, f"{name}: pages with almost no text -> {blank}"


@pytest.mark.parametrize("name", sorted(DAY_PDFS))
def test_pdf_names_the_notebook_it_came_from(name: str) -> None:
    reader = _reader(name)
    text = "\n".join((page.extract_text() or "") for page in reader.pages)
    assert "notebooks/" in text, f"{name}: no notebook path in the document"
    assert ".ipynb" in text, f"{name}: no notebook file named in the document"


def test_interactive_sections_are_replaced_by_a_static_note() -> None:
    """ウィジェットは静的図＋注記に置き換える / widgets become a static figure and a note."""
    reader = _reader("Day03")
    text = "\n".join((page.extract_text() or "") for page in reader.pages)
    assert "ノートブック上での対話操作" in text, "the widget note is missing"
    assert "ipywidgets" not in text, "widget source code leaked into the PDF"


def test_wide_figures_use_a_landscape_page() -> None:
    """横長の図は横向きページに置く（縦向きで潰さない）/ wide figures get a landscape page."""
    reader = _reader("Day05")
    sizes = {(round(float(page.mediabox.width)), round(float(page.mediabox.height)))
             for page in reader.pages}
    assert any(width > height for width, height in sizes), "no landscape page: wide figures are squeezed"
    assert any(height > width for width, height in sizes), "no portrait page: text pages are missing"


def test_installation_and_regeneration_commands_are_documented() -> None:
    readme = (PDF_DIR / "README.md").read_text(encoding="utf-8")
    assert "python assets\\scripts\\export_explanations_pdf.py" in readme
    assert "requirements\\pdf.txt" in readme
    requirements = (COURSE_ROOT / "requirements" / "pdf.txt").read_text(encoding="utf-8")
    assert "reportlab" in requirements


@pytest.mark.parametrize("name,languages", [
    ("Day05", "ja_en"),
    ("Week1", "ja_en"),
    ("Week1", "ja_en_ne"),
])
def test_learner_pdfs_exclude_archived_test_images_and_worked_answers(name, languages) -> None:
    from PIL import Image

    forbidden_images = set()
    for filename in ("ref_anomaly_panels.png", "ref_comparison_5col.png"):
        with Image.open(COURSE_ROOT / "assets" / "reference_outputs" / filename) as image:
            forbidden_images.add((image.size, hashlib.sha256(image.convert("RGB").tobytes()).digest()))
    with Image.open(COURSE_ROOT / "assets" / "reference_outputs" / "teach_numeric_map_toy.png") as image:
        expected_toy = (image.size, hashlib.sha256(image.convert("RGB").tobytes()).digest())
    pypdf = pytest.importorskip("pypdf")
    reader = pypdf.PdfReader(str(PDF_DIR / f"{name}_explanation_{languages}.pdf"))
    day5_started = name == "Day05"
    day5_text = []
    toy_seen = False
    for page in reader.pages:
        text = page.extract_text() or ""
        if "notebooks/Day05_PatchCore/Day05_01_" in text:
            day5_started = True
        if day5_started:
            day5_text.append(text)
        for embedded in page.images:
            image = embedded.image.convert("RGB")
            fingerprint = (image.size, hashlib.sha256(image.tobytes()).digest())
            assert fingerprint not in forbidden_images, f"{name}: archived TEST panel embedded"
            toy_seen |= fingerprint == expected_toy
    text = "\n".join(day5_text)
    for evidence in ("21.439", "21.762", "black_spot_0000", "streak_0005"):
        assert evidence not in text, f"{name}: archived TEST worked answer {evidence}"
    assert "CALCULATED SYNTHETIC TOY" in text or "Calculated synthetic toy numeric map" in text
    assert "0.600" in text
    assert toy_seen, f"{name}: the declared synthetic toy was not embedded unchanged"
