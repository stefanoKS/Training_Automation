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

# Every trilingual booklet is Romanized (`ne-Latn`) now: the 16 notebook catalogs and the 12 learner
# documents were migrated, so no learner-facing PDF may still carry Devanagari.
ROMANIZED_PDFS = set(TRILINGUAL_PDFS)
ROMANIZED_MARKERS = ("chhannuhos", "natija", "tasbir", "garnuhos", "chha", "chhaina")

LEARNER_DOCUMENTS = [
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


def test_all_sixteen_catalogs_are_romanized(coverage) -> None:
    """全 16 冊のカタログがラテン文字であること / every notebook catalog is `ne-Latn`."""
    catalogs = sorted(CATALOG_DIR.glob("*.ne.md"))
    assert len(catalogs) == 16, f"expected 16 notebook catalogs, found {len(catalogs)}"
    devanagari = {path.name: len(DEVANAGARI_RE.findall(path.read_text(encoding="utf-8")))
                  for path in catalogs if DEVANAGARI_RE.search(path.read_text(encoding="utf-8"))}
    assert devanagari == {}, f"catalogs still carrying Devanagari: {devanagari}"
    scripts = {path.name: coverage.catalog_script(path) for path in catalogs}
    assert set(scripts.values()) == {"romanized"}, f"mixed-script catalogs: {scripts}"


def test_no_devanagari_survives_in_any_notebook_region(coverage) -> None:
    """ノートブック本文のネパール語領域もラテン文字であること / no Devanagari in the notebooks."""
    report = coverage.run()
    survivors = {item["path"]: item["scripts"].count("devanagari")
                 for item in report["notebooks"] if "devanagari" in item["scripts"]}
    assert survivors == {}, f"Devanagari Nepali regions remain: {survivors}"
    assert report["totals"]["devanagari_blocks"] == 0
    assert report["totals"]["romanized_blocks"] > 1000


@pytest.mark.parametrize("name", LEARNER_DOCUMENTS)
def test_all_twelve_documents_are_romanized(name, doc_applier) -> None:
    text = (COURSE_ROOT / name).read_text(encoding="utf-8")
    regions = [match.group("body") for match in doc_applier.REGION_RE.finditer(text)]
    assert regions, f"{name}: no Nepali region"
    for body in regions:
        assert not DEVANAGARI_RE.search(body), f"{name}: Devanagari Nepali remains"


def test_notebook_applier_is_idempotent(notebook_applier) -> None:
    """A second run must not change a single byte. / 2 回目は 1 バイトも変えない."""
    for catalog_path in sorted(CATALOG_DIR.glob("*.ne.md")):
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
    """三言語版はラテン文字のネパール語を検索できる文字層で持つこと / a searchable ne-Latn layer."""
    pdfium = pytest.importorskip("pypdfium2",
                                 reason="PDF tooling is optional (requirements/pdf.txt)")
    path = PDF_DIR / name
    if not path.is_file():
        pytest.skip(f"{name} has not been built yet")
    document = pdfium.PdfDocument(str(path))
    text = "\n".join(document[index].get_textpage().get_text_range()
                     for index in range(len(document)))
    assert not DEVANAGARI_RE.search(text), f"{name}: Devanagari is back in a learner booklet"
    lowered = text.lower()
    assert any(marker in lowered for marker in ROMANIZED_MARKERS), (
        f"{name}: no Romanized Nepali marker in the text layer")


@pytest.mark.parametrize("name", sorted(ROMANIZED_PDFS))
def test_migrated_pdfs_carry_romanized_nepali_only(name: str) -> None:
    pdfium = pytest.importorskip("pypdfium2",
                                 reason="PDF tooling is optional (requirements/pdf.txt)")
    path = PDF_DIR / name
    if not path.is_file():
        pytest.skip(f"{name} has not been built yet")
    document = pdfium.PdfDocument(str(path))
    text = "\n".join(document[index].get_textpage().get_text_range()
                     for index in range(len(document)))
    assert not DEVANAGARI_RE.search(text), f"{name}: Devanagari survived the migration"
    lowered = text.lower()
    hits = [marker for marker in ROMANIZED_MARKERS if marker in lowered]
    assert len(hits) >= 2, f"{name}: expected Romanized Nepali prose, found {hits}"


BILINGUAL_PDFS = [
    "Day01_explanation_ja_en.pdf",
    "Day02_explanation_ja_en.pdf",
    "Day03_explanation_ja_en.pdf",
    "Day04_explanation_ja_en.pdf",
    "Day05_explanation_ja_en.pdf",
    "Week1_explanation_ja_en.pdf",
]


@pytest.mark.parametrize("name", BILINGUAL_PDFS)
def test_bilingual_booklet_exists(name: str) -> None:
    path = PDF_DIR / name
    assert path.is_file(), f"the bilingual booklet {name} disappeared"
    assert path.stat().st_size > 10_000


@pytest.mark.parametrize("name", BILINGUAL_PDFS)
def test_bilingual_booklet_carries_no_nepali(name: str) -> None:
    """日英版にネパール語の本文やマーカーが混ざらないこと / no Nepali region or marker leaks in."""
    pdfium = pytest.importorskip("pypdfium2",
                                 reason="PDF tooling is optional (requirements/pdf.txt)")
    path = PDF_DIR / name
    if not path.is_file():
        pytest.skip(f"{name} has not been built yet")
    document = pdfium.PdfDocument(str(path))
    text = "\n".join(document[index].get_textpage().get_text_range()
                     for index in range(len(document)))
    assert "ne:begin" not in text and "ne:end" not in text, f"{name}: region markers printed"
    assert not DEVANAGARI_RE.search(text), f"{name}: Devanagari Nepali printed"
    lowered = text.lower()
    leaked = [marker for marker in ROMANIZED_MARKERS if marker in lowered]
    assert not leaked, f"{name}: Romanized Nepali printed in a Japanese + English booklet {leaked}"


def test_bilingual_exporter_strips_the_nepali_regions() -> None:
    """組版側で領域を落とすこと / the typesetter removes the regions itself."""
    exporter = _load("export_explanations_pdf")
    text = ("日本語の説明。\n\n<!-- ne:begin end -->\ndin 2 Notebook 01: parichay\n<!-- ne:end -->\n\n"
            "English explanation.\n\n<!-- ne:begin after-heading -->\n**chitra**\n<!-- ne:end -->\n")
    stripped = exporter.strip_nepali(text)
    assert "din 2 Notebook 01" not in stripped and "**chitra**" not in stripped
    assert "ne:begin" not in stripped and "ne:end" not in stripped
    assert "日本語の説明。" in stripped and "English explanation." in stripped
    assert stripped == exporter.strip_nepali(stripped)


def test_doc_applier_keeps_the_japanese_and_english(doc_applier) -> None:
    """The document applier must not eat the prose it was layered on."""
    text = (COURSE_ROOT / "START_HERE.md").read_text(encoding="utf-8")
    original = doc_applier.strip_regions(text)
    assert len(original) > 0.5 * len(text)


def test_bilingual_day02_booklet_carries_the_revised_figure() -> None:
    """Day 2 の図を直したので、二言語版も作り直していること / the bilingual Day 2 rebuild happened."""
    pdfium = pytest.importorskip("pypdfium2",
                                 reason="PDF tooling is optional (requirements/pdf.txt)")
    path = PDF_DIR / "Day02_explanation_ja_en.pdf"
    if not path.is_file():
        pytest.skip("Day02_explanation_ja_en.pdf has not been built yet")
    document = pdfium.PdfDocument(str(path))
    text = "\n".join(document[index].get_textpage().get_text_range()
                     for index in range(len(document)))
    assert "外部輪郭" in text, "the revised Day 2 figure caption is missing"
    assert "連結領域の数" not in text, "the old dual-axis wording is still in the booklet"


# 承認済みの日本語・英語を翻訳が置き換えていないこと / the approved prose survives every rerun
APPROVED_PROSE = [
    ("Day01_01_Introduction_to_AI", "21e8248a",
     "# 第1日 ノートブック01：AIとは何か", "# Day 1 Notebook 01: Introduction to AI"),
    ("Day02_01_Python_Basics", "79dc91db",
     "# 第2日 ノートブック01：Python 入門", "# Day 2 Notebook 01: Python for Absolute Beginners"),
    ("Day02_01_Python_Basics", "fcc49434",
     "## このノートブックの位置 / Where this notebook sits", "| 所要時間 / Duration | 125 分 / 125 minutes |"),
    ("Day05_03_YOLO_vs_PatchCore", "clarity-freeze-prompt",
     "#### 必須：固定と未使用性を記録 / Required: record freeze and holdout status",
     "`TEST_ALREADY_SEEN=True` のままにします。"),
]


@pytest.mark.parametrize("stem, cell_id, japanese, english", APPROVED_PROSE)
def test_approved_japanese_and_english_survive(stem, cell_id, japanese, english,
                                               notebook_applier) -> None:
    path, = notebook_applier.course_notebooks(COURSE_ROOT / "notebooks", f"{stem}.ipynb")
    notebook = json.loads(path.read_text(encoding="utf-8"))
    cell = next(item for item in notebook["cells"] if item.get("id") == cell_id)
    outside = notebook_applier.strip_regions("".join(cell["source"]))
    assert japanese in outside
    assert english in outside


def test_every_notebook_still_carries_japanese_outside_the_regions(notebook_applier) -> None:
    thin = {}
    for path in notebook_applier.course_notebooks(COURSE_ROOT / "notebooks"):
        notebook = json.loads(path.read_text(encoding="utf-8"))
        outside = "".join(notebook_applier.strip_regions("".join(cell["source"]))
                          for cell in notebook["cells"] if cell["cell_type"] == "markdown")
        japanese = len(re.findall(r"[\u3040-\u30ff\u4e00-\u9fff]", outside))
        assert japanese > 1000, f"{path.name}: only {japanese} Japanese characters left"
