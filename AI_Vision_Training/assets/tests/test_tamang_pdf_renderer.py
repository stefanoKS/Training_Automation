"""タマン語 PDF の描画経路 / the rendering path a ``*_ja_en_taj.pdf`` would use.

No Tamang booklet can be built yet (the localization gate blocks it), so this module verifies the
parts that do not depend on the text being approved:

* Devanagari is shaped by the same Chromium/HarfBuzz path and lands in the PDF as **searchable
  Unicode**, not as private-use glyphs;
* headings, tables, images, links and page breaks survive that path;
* ``export_trilingual_pdf --locale taj`` refuses to write ``*_ja_en_taj.pdf`` while the gate fails,
  and never renames a Nepali booklet into a Tamang one.

The Devanagari sample here is the attested name of the language (``तामाङ``), used as a *rendering*
fixture — it is not presented as a translation of any lesson.
"""

from __future__ import annotations

import json
import sys
from dataclasses import replace
from pathlib import Path

import pytest

pytest.importorskip("playwright.sync_api")
pytest.importorskip("pypdfium2")

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "assets" / "scripts"))

import export_trilingual_pdf as exporter  # noqa: E402
import apply_docs  # noqa: E402
import apply_translations  # noqa: E402
import check_localization_coverage as coverage  # noqa: E402
import i18n_locales  # noqa: E402
from test_tamang_localization import review_header  # noqa: E402

SAMPLE = "तामाङ भाषा"


@pytest.fixture(scope="module")
def rendered(tmp_path_factory) -> dict:
    folder = tmp_path_factory.mktemp("taj-render")
    image = ROOT / "assets" / "diagrams" / "diagram_dataset_split.png"
    html = f"""<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><style>
body {{ font-family: "Yu Gothic", "Nirmala UI", sans-serif; }}
table {{ border-collapse: collapse; }}
td, th {{ border: 1px solid #888; padding: 4px; }}
p {{ page-break-before: always; }}
</style></head><body>
<h1 lang="taj-Deva">固定の記録 / freeze record</h1>
<p lang="taj-Deva">{SAMPLE}</p>
<table><thead><tr><th>手順</th><th>Step</th></tr></thead>
<tbody><tr><td>1</td><td>split</td></tr></tbody></table>
<img src="{image.as_uri()}" style="width:80mm"/>
<p><a href="https://example.org/docs">link</a></p>
</body></html>"""
    html_path = folder / "sample.html"
    html_path.write_text(html, encoding="utf-8")
    pdf_path = folder / "sample.pdf"
    exporter.render(html_path, pdf_path, "taj rendering fixture")
    return {"pdf": pdf_path, "texts": exporter.page_texts(pdf_path)}


def test_devanagari_survives_as_searchable_text(rendered) -> None:
    text = "\n".join(rendered["texts"])
    assert SAMPLE in text, "the Devanagari sample must be searchable in the PDF text layer"
    assert "\u0924\u093e\u092e\u093e\u0919" in text  # तामाङ
    assert "freeze record" in text, "the Japanese/English heading must survive too"


def test_tables_and_links_survive_the_render(rendered) -> None:
    text = "\n".join(rendered["texts"])
    assert "split" in text and "手順" in text
    assert len(rendered["texts"]) >= 2, "the forced page break must produce a second page"


def test_the_gate_refuses_to_build_a_tamang_booklet(tmp_path) -> None:
    out = tmp_path / "pdf"
    out.mkdir()
    assert exporter.main(["--locale", "taj", "--only", "Day05", "--out", str(out)]) == 2
    assert not list(out.glob("*_ja_en_taj.pdf")), "no Tamang booklet may be produced yet"
    assert not list(out.glob("*.pdf"))


def test_switching_the_locale_does_not_relabel_the_nepali_booklets(tmp_path) -> None:
    exporter.configure_locale("ne")
    assert exporter.LOCALE.code == "ne"
    assert exporter.LANG_ATTR["ne"] == "ne-Latn"
    assert exporter.LOCALE.pdf_suffix() == "ja_en_ne"

    exporter.configure_locale("taj")
    assert exporter.LANG_ATTR["ne"] == "taj-Deva"
    assert exporter.LOCALE.pdf_suffix() == "ja_en_taj"
    # the Tamang build must not borrow the Romanized Nepali course title
    assert "hapta" not in exporter.COURSE_TITLE_NE
    exporter.configure_locale("ne")


# ---------------------------------------------------------------------------
# Day 5: one concept, three languages, one reading order
# ---------------------------------------------------------------------------

UNIT_JA = "しきい値は較正用データで決めます。"
UNIT_EN = "The threshold is chosen on the calibration data."
UNIT_TAJ = "तामाङ पाठ।"
ROW_JA = "低いしきい値"
ROW_EN = "low threshold"
ROW_TAJ = "तामाङ पंक्ति।"
CAPTION_JA = "図：較正で決めたしきい値。"
CAPTION_EN = "Figure: the threshold chosen on calibration."
CAPTION_TAJ = "तामाङ चित्र।"


def day5_cells(folder: Path) -> tuple[Path, list[dict]]:
    image = ROOT / "assets" / "diagrams" / "diagram_dataset_split.png"
    (folder / "split.png").write_bytes(image.read_bytes())
    cells = [
        {"cell_type": "markdown", "id": "concept",
         "source": "#### しきい値 / Threshold\n\n"
                   f"{UNIT_JA}\n\n{UNIT_EN}\n\n<!-- taj-unit: threshold -->\n"},
        {"cell_type": "markdown", "id": "row",
         "source": "| しきい値<br>threshold | 意味<br>meaning |\n| --- | --- |\n"
                   f"| {ROW_JA}<br>{ROW_EN} <!-- taj-row: low --> | 較正で決める<br>chosen on calibration |\n"},
        {"cell_type": "markdown", "id": "figure",
         "source": "![split](split.png)\n\n"
                   f"{CAPTION_JA}\n\n{CAPTION_EN}\n\n<!-- taj-unit: threshold-caption -->\n"},
        {"cell_type": "markdown", "id": "next",
         "source": "#### 次の概念 / Next concept\n\n次の説明。\n\nThe next explanation.\n\n"
                   "<!-- taj-unit: next-concept -->\n"},
    ]
    return folder, cells


def test_the_grouped_day5_layout_keeps_one_concept_in_one_reading_order(tmp_path) -> None:
    """日本語 → 英語 → タマン語が同じ概念の位置に並ぶこと / JA, EN, then Tamang per concept."""
    folder, cells = day5_cells(tmp_path)
    blocks = {
        "concept": [{"at": "unit:threshold", "text": UNIT_TAJ}],
        "row": [{"at": "row:low", "text": ROW_TAJ}],
        "figure": [{"at": "unit:threshold-caption", "text": CAPTION_TAJ}],
    }
    document = exporter.Document("", "", "")
    for cell in cells:
        source = "".join(cell["source"])
        filled = apply_translations.apply_blocks(source, blocks.get(cell["id"], []),
                                                 i18n_locales.locale("taj"))
        assert apply_translations.apply_blocks(filled, blocks.get(cell["id"], []),
                                               i18n_locales.locale("taj")) == filled
        document.add(exporter.markdown_cell_html(filled, folder, cell["id"], document))
    html = exporter.html_document(document)
    assert "ne:begin" not in html and "ne:end" not in html
    assert html.count("<img") == 1, "the figure appears once, not once per language"
    assert html.count("<table>") == 1, "the table appears once, not once per language"
    html_path = tmp_path / "grouped.html"
    html_path.write_text(html, encoding="utf-8")
    pdf_path = tmp_path / "grouped.pdf"
    exporter.render(html_path, pdf_path, "grouped Day 5 fixture")
    texts = exporter.page_texts(pdf_path)
    text = "\n".join(texts)
    assert "\ufffd" not in text, "the Devanagari text layer must be searchable Unicode"
    key = exporter._search_key(text)
    for marker in (UNIT_TAJ, ROW_TAJ, CAPTION_TAJ):
        assert exporter._search_key(marker) in key, marker
    assert key.index(exporter._search_key(UNIT_JA)) < key.index(exporter._search_key(UNIT_EN))
    assert key.index(exporter._search_key(UNIT_EN)) < key.index(exporter._search_key(UNIT_TAJ))
    assert key.index(exporter._search_key(CAPTION_EN)) < key.index(exporter._search_key(CAPTION_TAJ))
    assert "Hapta" not in text and "Pahile" not in text, "no legacy Nepali in the Day 5 layout"


def test_the_grouped_day5_layout_puts_the_row_text_inside_its_row(tmp_path) -> None:
    pdfium = pytest.importorskip("pypdfium2")
    folder, cells = day5_cells(tmp_path)
    document = exporter.Document("", "", "")
    for cell in cells:
        if cell["id"] != "row":
            continue
        filled = apply_translations.apply_blocks(
            "".join(cell["source"]), [{"at": "row:low", "text": ROW_TAJ}],
            i18n_locales.locale("taj"))
        document.add(exporter.markdown_cell_html(filled, folder, cell["id"], document))
    html_path = tmp_path / "row.html"
    html_path.write_text(exporter.html_document(document), encoding="utf-8")
    pdf_path = tmp_path / "row.pdf"
    exporter.render(html_path, pdf_path, "grouped row fixture")
    pdf = pdfium.PdfDocument(str(pdf_path))
    page = pdf[0]
    textpage = page.get_textpage()
    ja = textpage.search(ROW_JA).get_next()
    taj = textpage.search(ROW_TAJ).get_next()
    assert ja and taj, "both the Japanese label and the Tamang row text must render"
    ja_box = textpage.get_charbox(ja[0])
    taj_box = textpage.get_charbox(taj[0])
    assert taj_box[1] < ja_box[1], "the Tamang cell text sits underneath the Japanese in its row"
    assert abs(taj_box[0] - ja_box[0]) < 40, "and in the same cell, not in another column"


def test_the_grouped_day5_layout_keeps_the_tamang_caption_under_its_image(tmp_path) -> None:
    pdfium = pytest.importorskip("pypdfium2")
    folder, cells = day5_cells(tmp_path)
    document = exporter.Document("", "", "")
    cell = next(item for item in cells if item["id"] == "figure")
    filled = apply_translations.apply_blocks(
        "".join(cell["source"]), [{"at": "unit:threshold-caption", "text": CAPTION_TAJ}],
        i18n_locales.locale("taj"))
    document.add(exporter.markdown_cell_html(filled, folder, cell["id"], document))
    html_path = tmp_path / "caption.html"
    html_path.write_text(exporter.html_document(document), encoding="utf-8")
    pdf_path = tmp_path / "caption.pdf"
    exporter.render(html_path, pdf_path, "grouped caption fixture")
    pdf = pdfium.PdfDocument(str(pdf_path))
    page = pdf[0]
    textpage = page.get_textpage()
    images = [obj for obj in page.get_objects() if obj.type == pdfium.raw.FPDF_PAGEOBJ_IMAGE]
    assert images
    image_bottom = min(obj.get_bounds()[1] for obj in images)
    english = textpage.search(CAPTION_EN[:20]).get_next()
    tamang = textpage.search(CAPTION_TAJ).get_next()
    assert english and tamang
    english_bottom = textpage.get_charbox(english[0])[1]
    tamang_bottom = textpage.get_charbox(tamang[0])[1]
    assert 0 <= image_bottom - english_bottom < 100, "the captions stay under the picture"
    assert tamang_bottom < english_bottom, "the Tamang caption follows the English one"
    assert english_bottom - tamang_bottom < 100, "and stays in the same caption block"


def test_approved_fixture_exports_day_and_document_jobs(tmp_path, monkeypatch):
    pypdf = pytest.importorskip("pypdf")
    root = tmp_path / "course"
    nb_dir = root / "notebooks" / "Day01_AI_Fundamentals"
    nb_dir.mkdir(parents=True)
    loc = replace(i18n_locales.locale("taj"), confirmed=True)
    monkeypatch.setitem(i18n_locales.LOCALES, "taj", loc)
    monkeypatch.setattr(i18n_locales, "I18N_ROOT", root / "catalogs")
    for module in (coverage, exporter, apply_docs, apply_translations):
        monkeypatch.setattr(module, "COURSE_ROOT", root)
    monkeypatch.setattr(exporter, "NOTEBOOK_DIR", root / "notebooks")
    monkeypatch.setattr(coverage, "DOCUMENTS", ["fixture.md"])
    notebook = nb_dir / "Day01_01_Fixture.ipynb"
    figure = ROOT / "assets" / "diagrams" / "diagram_dataset_split.png"
    (nb_dir / "split.png").write_bytes(figure.read_bytes())
    notebook.write_text(json.dumps({"cells": [
        {"cell_type": "markdown", "id": "intro",
         "source": "# 固定の記録\n\n# Freeze record\n\n"
                   "日本語の説明。\n\nThe English explanation.\n\n"
                   "<!-- ne:begin end -->\nPahile secret legacy prose.\n<!-- ne:end -->\n"},
        {"cell_type": "markdown", "id": "figure",
         "source": "![split](split.png)\n\n図：分割\n\nFigure: Split diagram\n\n"
                   "<!-- ne:begin after-image:split.png -->\n"
                   "Chitrama secret caption.\n<!-- ne:end -->\n"},
        {"cell_type": "code", "id": "widget", "source": "import ipywidgets\n"},
        {"cell_type": "code", "id": "code", "source": "value = 42\n"},
    ]}, ensure_ascii=False), encoding="utf-8")
    name = "fixture.md"
    document = root / name
    document.write_text("# 手順 / Directions\n\nJA/EN document text.\n\n"
                        "<!-- ne:begin doc:abc -->\nLegacy document secret.\n<!-- ne:end -->\n",
                        encoding="utf-8")
    for kind in ("notebooks", "docs"):
        loc.catalog_dir(kind).mkdir(parents=True)
    notebook_catalog = coverage.catalogue_path(loc, notebook.stem)
    notebook_catalog.write_text(
        review_header(loc)
        + "<!-- taj-cell: intro | after-heading -->\n"
        + f"<!-- taj-pair: Freeze record -->\n# {SAMPLE}\n\n{SAMPLE}।\n"
        + "<!-- taj-status: intro approved -->\n"
        + f"<!-- taj-cell: figure | after-image:split.png -->\n<!-- taj-caption -->\n{SAMPLE}\n"
        + "<!-- taj-status: figure approved -->\n", encoding="utf-8")
    doc_catalog = coverage.doc_catalogue_path(loc, name)
    doc_catalog.write_text(review_header(loc) + f"<!-- taj-doc: {name} -->\n"
                           f"<!-- taj-section: # 手順 / Directions -->\n{SAMPLE}\n"
                           "<!-- taj-status: # 手順 / Directions | approved -->\n", encoding="utf-8")
    entries = apply_translations.parse_catalog(notebook_catalog, loc)
    assert apply_translations.apply_catalog(notebook, entries, True, loc)["changed"] == 2
    assert apply_translations.apply_catalog(notebook, entries, True, loc)["changed"] == 0
    assert apply_docs.apply_catalog(doc_catalog, True, loc)["changed"]
    assert not apply_docs.apply_catalog(doc_catalog, True, loc)["changed"]
    report = coverage.run(loc)
    assert coverage.gate_failures(report, loc) == []
    assert coverage.emit_pending_catalogs(loc, True) == []
    assert coverage.emit_pending_doc_catalogs(loc, True) == []
    assert "secret legacy prose" in notebook.read_text(encoding="utf-8")

    monkeypatch.setitem(exporter.DAYS, "Day01", dict(
        exporter.DAYS["Day01"], notebooks=[notebook.stem]))
    monkeypatch.setattr(exporter, "JOBS", [("Day01", ["Day01"], "Day01 fixture")])
    monkeypatch.setattr(exporter, "DOC_JOBS", [dict(
        exporter.DOC_JOBS[1], name="Fixture", sources=[
            (document, "手順 / Directions", "Suru garne tarika")])])
    rendered_html = []
    original_render = exporter.render

    def record_html(html_path, pdf_path, label):
        rendered_html.append(html_path.read_text(encoding="utf-8"))
        original_render(html_path, pdf_path, label)

    monkeypatch.setattr(exporter, "render", record_html)
    out = tmp_path / "pdf"
    try:
        assert exporter.main(["--locale", "taj", "--out", str(out)]) == 0
        # Exercise the default example-output message too (no borrowed Nepali fallbacks).
        example = exporter.markdown_cell_html(
            "## 実行結果の例\n## Expected output", nb_dir, "example",
            exporter.Document("", "", ""))
        assert "Run the notebook to see this output." in example
        assert "ne-Latn" not in example
    finally:
        exporter.configure_locale("ne")

    banned = ("ne-Latn", "Nepali", "Hapta", "Poorwashart", "Bishayasoochi", "udaharan",
              "Yo bhaag", "Suru garne tarika", "Pahile", "Chitrama", "Legacy document secret")
    assert len(rendered_html) == 4  # each branch ran both layout passes
    for markup in rendered_html:
        assert f'lang="taj-Deva">{SAMPLE}' in markup
        assert not (leaked := [token for token in banned if token in markup]), leaked
    assert 'class="cap ne" lang="taj-Deva"' in rendered_html[1]
    assert "interactive in the notebook only" in rendered_html[1]
    assert "value = 42" in rendered_html[1]

    for filename, content in (
        ("Day01_explanation_ja_en_taj.pdf", ("Freeze record", "固定の記録", "Figure: Split diagram")),
        ("Fixture_ja_en_taj.pdf", ("Directions", "手順", "JA/EN document text.")),
    ):
        pdf_path = out / filename
        pdf = pypdf.PdfReader(pdf_path)
        text = "\n".join(exporter.page_texts(pdf_path))
        assert SAMPLE in text and "\ufffd" not in text
        assert all(token in text for token in content)
        assert not (leaked := [token for token in banned if token in text]), leaked
        assert "Tamang (taj-Deva)" in pdf.metadata.subject
        assert pdf.outline
        fonts = {str(ref.get_object()["/BaseFont"])
                 for page in pdf.pages
                 for ref in page["/Resources"].get("/Font", {}).get_object().values()}
        assert any(any(font in name for font in ("Nirmala", "Devanagari", "Mangal"))
                   for name in fonts), fonts
        if filename.startswith("Day"):
            assert any(page.images for page in pdf.pages)
