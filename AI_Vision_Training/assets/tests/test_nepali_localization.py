"""ネパール語ローカライズのテスト / Nepali localization tests.

The Nepali text lives in sidecar catalogs and is applied by
``assets/scripts/apply_nepali_translations.py`` (notebooks) and ``apply_nepali_docs.py``
(documents). These tests guard the three things that have actually broken during this work:

1. the applier is **idempotent** and leaves code, outputs and the original Japanese/English alone;
2. every Markdown cell either carries Nepali or is a documented exemption;
3. the tri-language PDFs keep a **searchable** Devanagari text layer.
"""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

import pytest

COURSE_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = COURSE_ROOT / "assets" / "scripts"
PDF_DIR = COURSE_ROOT / "docs" / "pdf"
CATALOG_DIR = COURSE_ROOT / "assets" / "i18n" / "ne" / "notebooks"
DOC_CATALOG_DIR = COURSE_ROOT / "assets" / "i18n" / "ne" / "docs"

DEVANAGARI_RE = re.compile(r"[\u0900-\u097f]")
NE_SPLIT_RE = re.compile(r"[\u0900-\u097f][ \t\u00a0]+[\u093e-\u094f\u0962\u0963]")

TRILINGUAL_PDFS = [
    "Day01_explanation_ja_en_ne.pdf",
    "Day02_explanation_ja_en_ne.pdf",
    "Day03_explanation_ja_en_ne.pdf",
    "Day04_explanation_ja_en_ne.pdf",
    "Day05_explanation_ja_en_ne.pdf",
    "Week1_explanation_ja_en_ne.pdf",
    "Setup_ja_en_ne.pdf",
    "Installation_Guide_ja_en_ne.pdf",
    "Repository_Guide_ja_en_ne.pdf",
    "Course_Syllabus_ja_en_ne.pdf",
]

if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def coverage():
    return _load("check_nepali_coverage")


@pytest.fixture(scope="module")
def notebook_applier():
    return _load("apply_nepali_translations")


@pytest.fixture(scope="module")
def doc_applier():
    return _load("apply_nepali_docs")


def test_every_markdown_cell_is_translated_or_exempt(coverage) -> None:
    report = coverage.run()
    missing = {item["path"]: item["missing"] for item in report["notebooks"] if item["missing"]}
    assert missing == {}, f"Markdown cells without Nepali: {missing}"
    assert report["totals"]["translated"] > 0


def test_nepali_has_no_hindi_or_placeholder_text(coverage) -> None:
    report = coverage.run()
    problems = {item["path"]: item["forbidden"]
                for item in report["notebooks"] + report["documents"] if item["forbidden"]}
    assert problems == {}, f"forbidden Nepali content: {problems}"


def test_devanagari_only_lives_inside_marked_regions(coverage) -> None:
    report = coverage.run()
    stray = {item["path"]: item["stray_devanagari"]
             for item in report["notebooks"] if item["stray_devanagari"]}
    assert stray == {}, f"Devanagari outside a Nepali region: {stray}"


def test_every_document_carries_nepali(coverage) -> None:
    report = coverage.run()
    missing = [item["path"] for item in report["documents"] if not item["regions"]]
    assert missing == [], f"documents without Nepali: {missing}"


def test_catalogs_cover_exactly_the_shipped_notebooks(coverage) -> None:
    assert coverage.catalogs_match_notebooks() == []


def test_notebook_applier_is_idempotent(notebook_applier) -> None:
    """A second run must not change a single byte. / 2 回目は 1 バイトも変えない."""
    for catalog_path in sorted(CATALOG_DIR.glob("*.ne.md"))[:4]:
        entries = notebook_applier.parse_catalog(catalog_path)
        stem = catalog_path.name[: -len(".ne.md")]
        matches = notebook_applier.course_notebooks(COURSE_ROOT / "notebooks", f"{stem}.ipynb")
        assert len(matches) == 1, f"{stem}: expected one notebook"
        notebook = json.loads(matches[0].read_text(encoding="utf-8"))
        by_id = {cell.get("id"): cell for cell in notebook["cells"]}
        for cell_id, blocks in entries.items():
            cell = by_id.get(cell_id)
            assert cell is not None, f"{stem}: {cell_id} is not a cell of the notebook"
            source = "".join(cell["source"])
            once = notebook_applier.apply_blocks(source, blocks)
            twice = notebook_applier.apply_blocks(once, blocks)
            assert once == twice, f"{stem}: {cell_id} is not idempotent"


def test_notebook_applier_keeps_the_original_text(notebook_applier) -> None:
    """Nepali is added; nothing already in the cell may be dropped."""
    catalog_path = sorted(CATALOG_DIR.glob("*.ne.md"))[0]
    entries = notebook_applier.parse_catalog(catalog_path)
    stem = catalog_path.name[: -len(".ne.md")]
    path = notebook_applier.course_notebooks(COURSE_ROOT / "notebooks", f"{stem}.ipynb")[0]
    notebook = json.loads(path.read_text(encoding="utf-8"))
    by_id = {cell.get("id"): cell for cell in notebook["cells"]}
    for cell_id, blocks in entries.items():
        source = "".join(by_id[cell_id]["source"])
        original = notebook_applier.strip_regions(source)
        updated = notebook_applier.apply_blocks(source, blocks)
        assert notebook_applier.strip_regions(updated) == original


def test_doc_applier_header_must_exist(doc_applier) -> None:
    """Anchoring on a heading means a renamed heading fails loudly instead of silently."""
    with pytest.raises(doc_applier.CatalogError):
        doc_applier.section_bounds(["# a", "## b"], "## missing")
    with pytest.raises(doc_applier.CatalogError):
        doc_applier.section_bounds(["## 1. one", "## 1. two"], "## 1.")


def test_doc_applier_is_idempotent(doc_applier) -> None:
    for catalog_path in sorted(DOC_CATALOG_DIR.glob("*.ne.md")):
        target_rel, blocks = doc_applier.parse_catalog(catalog_path)
        text = (COURSE_ROOT / target_rel).read_text(encoding="utf-8")
        once = doc_applier.apply_blocks(doc_applier.strip_regions(text), blocks)
        twice = doc_applier.apply_blocks(once, blocks)
        assert once == twice, f"{target_rel}: not idempotent"


@pytest.mark.parametrize("name", ["START_HERE.md", "README.md",
                                 "docs/troubleshooting/installation.md"])
def test_nepali_keeps_each_actionable_cmd_line(name, doc_applier) -> None:
    text = (COURSE_ROOT / name).read_text(encoding="utf-8")
    original = doc_applier.strip_regions(text)
    nepali = "\n".join(match.group("body") for match in doc_applier.REGION_RE.finditer(text))
    for block in re.findall(r"```cmd\n(.*?)```", original, re.S):
        for line in block.splitlines():
            if line.strip() and not line.startswith("REM "):
                assert line in nepali, (name, line)


def test_nepali_timetable_keeps_every_window_and_notebook_part(doc_applier) -> None:
    text = (COURSE_ROOT / "COURSE_SYLLABUS.md").read_text(encoding="utf-8")
    original = doc_applier.strip_regions(text)
    nepali = "\n".join(match.group("body") for match in doc_applier.REGION_RE.finditer(text))
    pattern = r"^\| (\d\d:\d\d–\d\d:\d\d) \| (\d+) \| ([^|]+) \| ([^|]+) \|"
    original_rows = re.findall(pattern, original, re.M)
    nepali_rows = re.findall(pattern, nepali, re.M)
    assert [(r[0], r[1]) for r in nepali_rows] == [(r[0], r[1]) for r in original_rows]
    for source, translated in zip(original_rows, nepali_rows):
        tokens = r"`Day\d\d_\d\d`|Part \d+(?:–\d+)?"
        assert list(dict.fromkeys(re.findall(tokens, source[3]))) == list(
            dict.fromkeys(re.findall(tokens, translated[3])))


@pytest.mark.parametrize("name", TRILINGUAL_PDFS)
def test_trilingual_pdf_exists(name: str) -> None:
    path = PDF_DIR / name
    assert path.is_file(), f"missing {name}; run assets/scripts/export_trilingual_pdf.py"


@pytest.mark.parametrize("name", TRILINGUAL_PDFS)
def test_trilingual_pdf_text_layer_is_searchable(name: str) -> None:
    """Devanagari must extract without spurious spaces, or the PDF cannot be searched."""
    pdfium = pytest.importorskip("pypdfium2",
                                 reason="PDF tooling is optional (requirements/pdf.txt)")
    path = PDF_DIR / name
    if not path.is_file():
        pytest.skip(f"{name} has not been built yet")
    document = pdfium.PdfDocument(str(path))
    text = "\n".join(document[index].get_textpage().get_text_range()
                     for index in range(len(document)))
    assert DEVANAGARI_RE.search(text), f"{name}: no Devanagari in the text layer"
    split = NE_SPLIT_RE.findall(text)
    assert not split, f"{name}: {len(split)} Devanagari word(s) split by a space"


def test_original_japanese_english_pdfs_are_untouched() -> None:
    """The 2026-11-15 booklets must not be regenerated by the tri-language exporter."""
    for name in ("Day01_explanation_ja_en.pdf", "Week1_explanation_ja_en.pdf"):
        path = PDF_DIR / name
        assert path.is_file(), f"the original booklet {name} disappeared"
