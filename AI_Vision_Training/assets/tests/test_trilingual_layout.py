"""Semantic alignment regressions; no notebook execution or figure generation."""
from __future__ import annotations

import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "assets" / "scripts"))

import apply_nepali_translations as applier
import export_trilingual_pdf as exporter
from course_notebooks import course_notebooks

CASES = [
    ("00_Environment_Setup", "79328757", "f98449a1", "teach_setup_jupyter_ui.png", "Setup"),
    ("Day02_03_OpenCV_Image_Processing", "e15c580c", "audit-teach_opencv_pixel_pipeline",
     "teach_opencv_pixel_pipeline.svg", "Day02_explanation"),
    ("Day05_03_YOLO_vs_PatchCore", "3d343aab", "fig-teach_threshold_freeze",
     "teach_threshold_freeze.png", "Day05_explanation"),
]


def lesson(stem):
    path, = course_notebooks(ROOT / "notebooks", stem + ".ipynb")
    nb = json.loads(path.read_text(encoding="utf-8"))
    return path, {c["id"]: "".join(c["source"]) for c in nb["cells"]}


@pytest.mark.parametrize("stem,heading_id,figure_id,image,book", CASES)
def test_cited_heading_forms_one_semantic_heading(stem, heading_id, figure_id, image, book):
    path, cells = lesson(stem)
    doc = exporter.Document("", "", "")
    tree = ET.fromstring("<main>" + exporter.markdown_cell_html(
        cells[heading_id], path.parent, heading_id, doc) + "</main>")
    headings = [node for node in tree if re.fullmatch("h[1-4]", node.tag)]
    assert len(headings) == len(doc.toc) == 1
    assert [span.attrib["class"] for span in headings[0].findall("span")] == ["ja", "en", "ne"]
    assert all("".join(span.itertext()).strip() for span in headings[0].findall("span"))
    assert not re.search(r"^#{1,4} .*[\u0900-\u097f]", cells[heading_id], re.M)
    # Original body paragraphs remain after the grouped heading, in source order.
    original = applier.strip_regions(cells[heading_id])
    assert len(tree.findall("p")) > 2
    assert original.index(doc.toc[0].ja) < original.index(doc.toc[0].en)


def test_only_declared_pairs_merge_and_code_comments_are_not_headings():
    text = ("### 日本語の話\n\n説明です。\n\n### A different concept\n\nEnglish body.\n\n"
            "```python\n# a code comment\n```\n")
    doc = exporter.Document("", "", "")
    markup = exporter.markdown_cell_html(text, ROOT, "distinct", doc)
    assert len(doc.toc) == 2
    assert doc.toc[0].en is None
    assert doc.toc[1].ja == ""
    assert '<span class="ja"></span>' not in markup
    assert "# a code comment" in markup


def test_all_declared_pairs_are_unique_and_all_catalogs_are_idempotent():
    for path in course_notebooks(ROOT / "notebooks"):
        entries = applier.parse_catalog(applier.CATALOG_DIR / (path.stem + ".ne.md"))
        for cell in json.loads(path.read_text(encoding="utf-8"))["cells"]:
            if cell["cell_type"] != "markdown":
                continue
            text = "".join(cell["source"])
            if cell["id"] in entries:
                updated = applier.apply_blocks(text, entries[cell["id"]])
                assert updated == text
                assert applier.strip_regions(updated) == applier.strip_regions(text)
            doc = exporter.Document("", "", "")
            exporter.markdown_cell_html(text, path.parent, cell["id"], doc)
            for title in re.findall(r"<!-- ne-pair: (.+) -->", text):
                matches = [h for h in doc.toc if h.en == title]
                assert len(matches) == 1, (path, cell["id"], title)
                assert matches[0].ja and matches[0].ne


def test_missing_or_duplicate_pair_target_fails():
    text = ("### 日本語\n\n<!-- ne:begin after-heading -->\n**नेपाली शीर्षक**\n"
            "<!-- ne-pair: English title -->\n<!-- ne:end -->\n\n")
    for suffix in ("", "### English title\n\n### English title\n"):
        with pytest.raises(ValueError, match="ambiguous or missing"):
            exporter.markdown_cell_html(text + suffix, ROOT, "bad", exporter.Document("", "", ""))


def test_every_visual_region_is_inside_its_exact_figure():
    for path in course_notebooks(ROOT / "notebooks"):
        for cell in json.loads(path.read_text(encoding="utf-8"))["cells"]:
            if cell["cell_type"] != "markdown":
                continue
            text = "".join(cell["source"])
            regions = {a.partition(":")[2]: r["body"] for a, r in applier.parse_regions(text).items()
                       if a.startswith("after-image:")}
            if not exporter.IMAGE_RE.search(text):
                continue
            assert regions, (path, cell["id"])
            tree = ET.fromstring("<main>" + exporter.markdown_cell_html(
                text, path.parent, cell["id"], exporter.Document("", "", "")) + "</main>")
            figures = {node.attrib["data-image"]: node for node in tree.findall("div")
                       if "data-image" in node.attrib}
            for target, body in regions.items():
                figure = figures[Path(target).name]
                assert figure.find("img") is not None
                for paragraph in body.split("\n\n"):
                    if applier.CAPTION_RE.match(paragraph):
                        caption = " ".join(paragraph.splitlines())
                        expected = ET.fromstring("<p>" + exporter.inline(caption) + "</p>")
                        assert "".join(expected.itertext()) in [
                            "".join(c.itertext()) for c in figure.findall("div")
                            if c.attrib.get("class") == "cap ne"]
                        break
                if "ध्यान दिनुपर्ने कुरा" in body:
                    notes = figure.find("div[@class='visual-notes']")
                    assert "ध्यान दिनुपर्ने कुरा" in "".join(notes.itertext())


def test_multiple_image_anchors_keep_captions_separate_and_reject_bad_targets():
    first = "../../assets/diagrams/teach_setup_jupyter_ui.png"
    second = "../../assets/diagrams/teach_threshold_freeze.png"
    path, _ = lesson("00_Environment_Setup")
    original = f"![]({first})\n\nFigure: first.\n\n![]({second})\n\nFigure: second.\n"
    blocks = [{"at": "after-image:" + first, "text": "चित्र: पहिलो।\n\n**सोच्नुहोस्**\n\nकिन?"},
              {"at": "after-image:" + second, "text": "चित्र: दोस्रो।"}]
    source = applier.apply_blocks(original, blocks)
    assert applier.apply_blocks(source, blocks) == source
    assert applier.strip_regions(source) == original
    tree = ET.fromstring("<main>" + exporter.markdown_cell_html(
        source, path.parent, "two", exporter.Document("", "", "")) + "</main>")
    figures = tree.findall("div")
    assert "पहिलो" in "".join(figures[0].itertext())
    assert "दोस्रो" not in "".join(figures[0].itertext())
    assert "दोस्रो" in "".join(figures[1].itertext())
    with pytest.raises(applier.CatalogError, match="expected one image"):
        applier.apply_blocks(original.replace(second, first), blocks)
    with pytest.raises(applier.CatalogError, match="expected one image"):
        applier.apply_blocks(original, [{"at": "after-image:missing.png", "text": "चित्र: छैन।"}])
    with pytest.raises(applier.CatalogError, match="expected one image"):
        applier.apply_blocks(source.replace(second, first), blocks)


def test_nepali_lesson_paragraph_is_not_promoted_to_a_caption():
    path, _ = lesson("00_Environment_Setup")
    target = "../../assets/diagrams/teach_setup_jupyter_ui.png"
    text = applier.apply_blocks(f"![]({target})\n", [{
        "at": "after-image:" + target,
        "text": "चित्र: क्याप्सन।\n\n**ध्यान दिनुपर्ने कुरा**\n\nचित्रमा अर्को व्याख्या छ।"}])
    tree = ET.fromstring("<main>" + exporter.markdown_cell_html(
        text, path.parent, "notes", exporter.Document("", "", "")) + "</main>")
    figure = tree.find("div")
    assert len(figure.findall("div[@class='cap ne']")) == 1
    assert "चित्रमा अर्को व्याख्या छ।" in "".join(
        figure.find("div[@class='visual-notes']").itertext())


def test_all_visual_explanations_fit_with_their_existing_images(tmp_path):
    pdfium = pytest.importorskip("pypdfium2")
    pytest.importorskip("playwright.sync_api")
    document = exporter.Document("", "", "")
    expected = []
    for path in course_notebooks(ROOT / "notebooks"):
        for cell in json.loads(path.read_text(encoding="utf-8"))["cells"]:
            if cell["cell_type"] != "markdown" or not exporter.IMAGE_RE.search("".join(cell["source"])):
                continue
            tree = ET.fromstring("<main>" + exporter.markdown_cell_html(
                "".join(cell["source"]), path.parent, cell["id"],
                exporter.Document("", "", "")) + "</main>")
            for figure in tree.findall("div"):
                if "data-image" not in figure.attrib:
                    continue
                document.add(ET.tostring(figure, encoding="unicode", method="html"))
                notes = "".join(figure.find("div[@class='visual-notes']").itertext())
                caption = figure.find("div[@class='cap ne']")
                text = "".join(caption.itertext()) if caption is not None else notes
                # 先頭 60 文字だけで探すと、同じ図を 2 つの授業で使ったときの共通の書き出しで衝突
                # します。同じページにある説明の末尾も条件に入れて、その図だけに絞ります。
                # The first 60 characters alone collide when one figure is reused in two lessons with
                # the same opening sentence, so the tail of its own notes identifies the page.
                expected.append((cell["id"], text[:60], notes[-60:]))
    html_path = tmp_path / "all-figures.html"
    html_path.write_text(exporter.html_document(document), encoding="utf-8")
    pdf_path = tmp_path / "all-figures.pdf"
    exporter.render(html_path, pdf_path, "visual explanation regression")
    pdf = pdfium.PdfDocument(str(pdf_path))
    texts = [exporter._search_key(page.get_textpage().get_text_range()) for page in pdf]
    for cell_id, first, last in expected:
        tail = exporter._search_key(last)
        hits = [i for i, text in enumerate(texts)
                if exporter._search_key(first) in text and tail in text]
        assert len(hits) == 1, cell_id
        assert any(obj.type == pdfium.raw.FPDF_PAGEOBJ_IMAGE
                   for obj in pdf[hits[0]].get_objects()), cell_id


def test_document_translation_anchors_render_without_notebook_anchor_validation():
    text = ("English instructions.\n\n<!-- ne:begin doc:67168a6814 -->\n"
            "नेपाली निर्देशन।\n<!-- ne:end -->\n")
    markup = exporter.markdown_cell_html(text, ROOT, "document", exporter.Document("", "", ""))
    assert "English instructions." in markup
    assert "नेपाली निर्देशन।" in markup
    assert "ne:begin" not in markup


def test_toc_matches_complete_headings_in_body_order_not_body_mentions():
    headings = [exporter.Heading(3, "日本語", "English title", "नेपाली शीर्षक", "first"),
                exporter.Heading(3, "日本語", "English title", "नेपाली शीर्षक", "second")]
    signature = "日本語\nEnglish title\nनेपाली शीर्षक"
    texts = ["TOC " + signature, "English title is mentioned here", signature, signature]
    pages = exporter.locate_headings(texts, headings, body_start=2)
    assert pages == {"first": 3, "second": 4}
    tree = ET.fromstring(exporter.toc_html(headings, pages))
    assert [(a.attrib["href"], a.find("span[@class='pg']").text)
            for a in tree.findall(".//a")] == [("#first", "3"), ("#second", "4")]
    assert all("नेपाली शीर्षक" in "".join(a.itertext()) for a in tree.findall(".//a"))
    with pytest.raises(ValueError, match="body marker missing"):
        exporter.body_start_page(["no sentinel"])


def test_body_sentinel_does_not_leak_onto_the_preceding_toc_page(tmp_path):
    pytest.importorskip("pypdfium2")
    pytest.importorskip("playwright.sync_api")
    heading = exporter.Heading(2, "日本語", "English title", "नेपाली शीर्षक", "body")
    document = exporter.Document("", "", "")
    document.add(exporter.toc_html([heading], {"body": 2}))
    document.add('<section class="section">' + exporter.SENTINEL_HTML
                 + exporter._heading_html(heading) + "</section>")
    html_path = tmp_path / "toc-boundary.html"
    html_path.write_text(exporter.html_document(document), encoding="utf-8")
    pdf_path = tmp_path / "toc-boundary.pdf"
    exporter.render(html_path, pdf_path, "body marker regression")
    texts = exporter.page_texts(pdf_path)
    start = exporter.body_start_page(texts)
    assert start == 2
    assert exporter.BODY_SENTINEL not in texts[0]
    assert exporter.locate_headings(texts, [heading], start) == {"body": 2}


def test_romanized_nepali_is_tagged_by_provenance_not_by_glyphs():
    text = ("### 見出し / Heading\n\n"
            "日本語の本文です。\n\n"
            "English body with the value and the model.\n\n"
            "<!-- ne:begin end -->\n"
            "Yo natija ho. Tasbir ra data ma chha. Garnuhos.\n"
            "<!-- ne:end -->\n")
    document = exporter.Document("", "", "")
    markup = exporter.markdown_cell_html(text, ROOT, "lang", document)
    assert '<p class="ne" lang="ne-Latn">Yo natija ho.' in markup
    assert 'class="ne">' not in markup, "every Nepali element must carry lang=ne-Latn"
    assert '<p class="en" lang="en">English body' in markup
    assert '<p class="ja" lang="ja">日本語の本文です。</p>' in markup


def test_english_paragraph_is_not_mistaken_for_nepali():
    markup = exporter.markdown_cell_html(
        "English body with the value and the model.\n", ROOT, "en", exporter.Document("", "", ""))
    assert 'class="ne"' not in markup
    assert 'lang="ne-Latn"' not in markup


def test_romanized_figure_caption_is_grouped_with_its_image():
    body = ("![](../../assets/diagrams/teach_threshold_freeze.png)\n\n"
            "Figure: an English caption.\n\n"
            "<!-- ne:begin after-image:../../assets/diagrams/teach_threshold_freeze.png -->\n"
            "Chitra: yo caption ho. **Dhyan dinuparne kura**\n\n"
            "Yo natija ho.\n"
            "<!-- ne:end -->\n")
    path, _ = lesson("Day05_03_YOLO_vs_PatchCore")
    markup = exporter.markdown_cell_html(body, path.parent, "fig", exporter.Document("", "", ""))
    assert '<div class="cap ne" lang="ne-Latn">Chitra: yo caption ho.' in markup
    assert 'lang="ne-Latn">Yo natija ho.' in markup


def test_font_preflight_fails_instead_of_accepting_generic_fallback():
    class Session:
        def send(self, name, args=None):
            return {"DOM.getDocument": {"root": {"nodeId": 1}},
                    "DOM.querySelector": {"nodeId": 2},
                    "CSS.getPlatformFontsForNode": {"fonts": [
                        {"familyName": "LastResort", "glyphCount": 4}]}}.get(name, {})

        def detach(self):
            pass

    page = SimpleNamespace(
        evaluate=lambda *args: None,
        locator=lambda *args: SimpleNamespace(evaluate=lambda *args: None),
        context=SimpleNamespace(new_cdp_session=lambda *args: Session()))
    with pytest.raises(RuntimeError, match="font coverage"):
        exporter.check_fonts(page, needs_devanagari=False)
    with pytest.raises(RuntimeError, match="font coverage"):
        exporter.check_fonts(page, needs_devanagari=True)


@pytest.mark.parametrize("key", exporter.DAY_ORDER + ["Week1"])
def test_distributed_toc_text_and_page_numbers_match_body(key):
    pytest.importorskip("pypdfium2")
    keys = exporter.DAY_ORDER if key == "Week1" else [key]
    doc, _ = exporter.build_document(keys, single=len(keys) == 1)
    texts = exporter.page_texts(ROOT / "docs" / "pdf" / f"{key}_explanation_ja_en_ne.pdf")
    start = exporter.body_start_page(texts)
    pages = exporter.locate_headings(texts, doc.toc, start)
    toc_text = exporter._search_key("".join(texts[1:start - 1]))
    for heading in doc.toc:
        if not heading.in_toc:
            continue
        signature = exporter._search_key("".join(
            part for part in (heading.ja, heading.en, heading.ne) if part))
        assert signature + str(pages[heading.anchor]) in toc_text, (key, heading.plain)


@pytest.mark.parametrize("stem,heading_id,figure_id,image,book", CASES)
def test_cited_caption_and_question_share_the_rendered_figure_page(
        tmp_path, stem, heading_id, figure_id, image, book):
    pdfium = pytest.importorskip("pypdfium2")
    pytest.importorskip("playwright.sync_api")
    path, cells = lesson(stem)
    doc = exporter.Document("", "", "")
    doc.add(exporter.markdown_cell_html(cells[figure_id], path.parent, figure_id, doc))
    html_path = tmp_path / "figure.html"
    html_path.write_text(exporter.html_document(doc), encoding="utf-8")
    pdf_path = tmp_path / "figure.pdf"
    exporter.render(html_path, pdf_path, "caption regression")
    pdf = pdfium.PdfDocument(str(pdf_path))
    pages = [pdf[index] for index in range(len(pdf))]
    body = cells[figure_id]
    caption_mark = "चित्र:" if "चित्र:" in body else "chitra:"
    question_mark = "सोच्नुहोस्" if "सोच्नुहोस्" in body else "sochnuhos"
    matches = [p for p in pages if caption_mark in p.get_textpage().get_text_range()]
    assert len(matches) == 1
    page = matches[0]
    textpage = page.get_textpage()
    assert question_mark in textpage.get_text_range()
    images = [obj for obj in page.get_objects() if obj.type == pdfium.raw.FPDF_PAGEOBJ_IMAGE]
    assert images
    start, count = textpage.search(caption_mark).get_next()
    caption_top = max(textpage.get_charbox(index)[3] for index in range(start, start + count))
    image_bottom = min(obj.get_bounds()[1] for obj in images)
    assert 0 <= image_bottom - caption_top < 100, "Nepali caption must be beneath its image"
    # Raster rendering is required as well as a searchable text layer.
    image = page.render(scale=1).to_pil()
    assert image.convert("L").getextrema()[0] < 100
